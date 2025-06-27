import random

import contextily
import matplotlib.pyplot as plt
import networkx
import osmnx
from matplotlib.lines import Line2D

from common.utils import MIN_SNOW_LEVEL, MAX_SNOW_LEVEL


def connect_sectors(sectors_graph, montreal_graph):
    montreal_projected = osmnx.project_graph(montreal_graph)

    # Composantes faiblement connectées
    components = list(networkx.weakly_connected_components(sectors_graph))

    if len(components) <= 1:
        return sectors_graph

    # Pour chaque paire de composantes, les connecter
    for i in range(len(components) - 1):
        comp1 = components[i]
        comp2 = components[i + 1]

        # Trouver les nœuds les plus proches entre les deux composantes
        min_dist = float("inf")
        best_pair = None

        for node1 in comp1:
            for node2 in comp2:
                if (
                    "x" in sectors_graph.nodes[node1]
                    and "x" in sectors_graph.nodes[node2]
                ):

                    x1, y1 = (
                        sectors_graph.nodes[node1]["x"],
                        sectors_graph.nodes[node1]["y"],
                    )
                    x2, y2 = (
                        sectors_graph.nodes[node2]["x"],
                        sectors_graph.nodes[node2]["y"],
                    )

                    dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

                    if dist < min_dist:
                        min_dist = dist
                        best_pair = (node1, node2)

        if best_pair:
            # Trouver le chemin dans le graphe de Montréal
            node1, node2 = best_pair

            # Trouver les nœuds correspondants dans montreal_graph
            nearest1 = osmnx.nearest_nodes(
                montreal_projected,
                sectors_graph.nodes[node1]["x"],
                sectors_graph.nodes[node1]["y"],
            )
            nearest2 = osmnx.nearest_nodes(
                montreal_projected,
                sectors_graph.nodes[node2]["x"],
                sectors_graph.nodes[node2]["y"],
            )

            try:
                # Chemin le plus court
                path = networkx.shortest_path(
                    montreal_projected, nearest1, nearest2, weight="length"
                )

                # Ajouter le chemin au graphe des secteurs
                for j in range(len(path) - 1):
                    n1, n2 = path[j], path[j + 1]

                    # Ajouter les nœuds du chemin
                    if n1 not in sectors_graph:
                        sectors_graph.add_node(n1, **montreal_projected.nodes[n1])
                    if n2 not in sectors_graph:
                        sectors_graph.add_node(n2, **montreal_projected.nodes[n2])

                    # Ajouter l'arête avec snow_level=0
                    if montreal_projected.has_edge(n1, n2):
                        edge_data = montreal_projected.edges[n1, n2, 0].copy()
                        edge_data["snow_level"] = 0
                        sectors_graph.add_edge(n1, n2, **edge_data)

            except networkx.NetworkXNoPath:
                # Si y'a pas de chemin, ça veut dire que c'est une connexion directe
                sectors_graph.add_edge(node1, node2, length=min_dist, snow_level=0)

    return sectors_graph


def get_edge_colors(graph, color, min_snow_level, max_snow_level):
    colors = []
    black_color = (0, 0, 0, 1.0)

    for u, v, k, data in graph.edges(keys=True, data=True):
        if "snow_level" not in data:
            colors.append(black_color)
            continue

        snow_level = data["snow_level"]
        if snow_level < min_snow_level or snow_level > max_snow_level:
            colors.append(black_color)
        else:
            colors.append(
                color((snow_level - min_snow_level) / (max_snow_level - min_snow_level))
            )
    return colors


def generate_random_snow_levels(graph, min_level=0, max_level=30):
    for u, v, k, data in graph.edges(keys=True, data=True):
        if data.get("snow_level") is None:
            data["snow_level"] = random.uniform(min_level, max_level)
    return graph


def show_plot_before_scan(graph):
    print("Affichage du graphe de Montréal sans les banlieues")
    fig, ax = plt.subplots(figsize=(60, 60), dpi=100)

    osmnx.plot_graph(
        graph,
        ax=ax,
        edge_color="black",
        edge_linewidth=3,
        node_size=10,
        node_color="red",
        show=False,
        close=False,
    )

    contextily.add_basemap(
        ax,
        crs=graph.graph["crs"],
        source=contextily.providers.OpenStreetMap.Mapnik,
        alpha=0.7,
    )

    legend_elements = [
        Line2D(
            [0],
            [0],
            color="black",
            lw=8,
            label=f"Routes",
        ),
    ]

    ax.legend(handles=legend_elements, loc="upper left", fontsize=50)
    plt.title(
        "Réseau routier de Montréal sans les banlieues avant analyse du drône",
        fontsize=60,
        fontweight="bold",
        pad=20,
    )

    plt.show()


def generate_plot_snow_level(graph, colormap):
    fig, ax = plt.subplots(figsize=(60, 60), dpi=100)

    osmnx.plot_graph(
        graph,
        ax=ax,
        edge_color=get_edge_colors(graph, colormap, MIN_SNOW_LEVEL, MAX_SNOW_LEVEL),
        edge_linewidth=2,
        node_size=0,
        show=False,
        close=False,
    )

    contextily.add_basemap(
        ax,
        crs=graph.graph["crs"],
        source=contextily.providers.OpenStreetMap.Mapnik,
        alpha=0.7,
    )

    legend_elements = [
        Line2D(
            [0],
            [0],
            color="black",
            lw=8,
            label=f"< {MIN_SNOW_LEVEL} cm ou > {MAX_SNOW_LEVEL} cm (pas de déneigement)",
        ),
        Line2D(
            [0],
            [0],
            color=colormap(1),
            lw=8,
            label=f"{MIN_SNOW_LEVEL} cm - {MAX_SNOW_LEVEL} cm (niveau de neige)",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="red",
            lw=0,
            markersize=10,
            label="Nœuds (routes)",
        ),
    ]

    ax.legend(handles=legend_elements, loc="upper left", fontsize=50)
    plt.title(
        "Réseau routier de Montréal sans les banlieues - Niveaux de neige",
        fontsize=60,
        fontweight="bold",
        pad=20,
    )

    plt.show()


def parcours_euler(montreal_graph):
    graph = montreal_graph.to_undirected()

    # Trouver toutes les composantes connexes
    components = list(networkx.connected_components(graph))

    all_paths = []

    for component in components:
        subgraph = graph.subgraph(component).copy()

        if networkx.is_eulerian(subgraph):
            path = list(networkx.eulerian_circuit(subgraph))
            all_paths.extend(path)

        elif networkx.is_semieulerian(subgraph):
            path = list(networkx.eulerian_path(subgraph))
            all_paths.extend(path)

        else:
            print(
                f"Composante non-eulérienne de taille {len(component)} - ajout d'arêtes"
            )

            # Nœuds de degré impair dans cette composante
            odd_nodes = [n for n in subgraph.nodes() if subgraph.degree(n) % 2 == 1]

            # Créer un multigraphe pour cette composante
            MG = networkx.MultiGraph(subgraph)

            # Coupler les nœuds impairs
            for i in range(0, len(odd_nodes) - 1, 2):
                try:
                    path = networkx.shortest_path(
                        subgraph, odd_nodes[i], odd_nodes[i + 1], weight="length"
                    )
                    for j in range(len(path) - 1):
                        MG.add_edge(path[j], path[j + 1])
                except networkx.NetworkXNoPath:
                    continue

            # Essayer de créer un circuit eulérien
            if networkx.is_eulerian(MG):
                path = list(networkx.eulerian_circuit(MG))
                all_paths.extend(path)
            elif networkx.is_semieulerian(MG):
                path = list(networkx.eulerian_path(MG))
                all_paths.extend(path)

    return all_paths


def afficher_chemin(graph, chemin):
    graph = graph.to_undirected()

    fig, ax = plt.subplots(figsize=(15, 15))

    contextily.add_basemap(
        ax,
        crs=graph.graph["crs"],
        source=contextily.providers.OpenStreetMap.Mapnik,
        alpha=0.7,
    )

    osmnx.plot_graph(
        graph,
        ax=ax,
        show=False,
        close=False,
        node_color="lightblue",
        node_size=1,
        edge_color="lightgray",
        edge_linewidth=0.5,
    )

    chemin_coords = []
    for i, (u, v) in enumerate(chemin):
        if i == 0:
            chemin_coords.append([graph.nodes[u]["y"], graph.nodes[u]["x"]])
        chemin_coords.append([graph.nodes[v]["y"], graph.nodes[v]["x"]])

    for i, (u, v) in enumerate(chemin):
        x1, y1 = graph.nodes[u]["x"], graph.nodes[u]["y"]
        x2, y2 = graph.nodes[v]["x"], graph.nodes[v]["y"]
        color = "yellow" if i == 0 else "red"
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", color=color, lw=0.5),
        )

    if chemin:
        start_node = chemin[0][0]
        end_node = chemin[-1][1]
        ax.scatter(
            graph.nodes[start_node]["x"],
            graph.nodes[start_node]["y"],
            c="green",
            s=100,
            marker="o",
            label="Début",
        )
        ax.scatter(
            graph.nodes[end_node]["x"],
            graph.nodes[end_node]["y"],
            c="blue",
            s=100,
            marker="s",
            label="Fin",
        )

    ax.legend()
    ax.set_title("Parcours Eulérien - Montréal")
    plt.tight_layout()
    plt.show()

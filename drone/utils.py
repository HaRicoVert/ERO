import random

import contextily
import matplotlib.pyplot as plt
import networkx
import osmnx
from matplotlib.lines import Line2D

from common.utils import MIN_SNOW_LEVEL, MAX_SNOW_LEVEL


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


import math


def calcul_cout(vehicule, distance_totale_km):
    if hasattr(vehicule, "cost_for_first_8hours"):
        temps_total_heures = distance_totale_km / vehicule.average_speed
        heures_facturees = math.ceil(temps_total_heures)

        cout_temps = 0
        heures_restantes = heures_facturees

        while heures_restantes > 0:
            if heures_restantes >= 8:
                cout_temps += vehicule.cost_for_first_8hours
                heures_restantes -= 8

                if heures_restantes >= 8:
                    cout_temps += vehicule.cost_for_next8hours
                    heures_restantes -= 8
                elif heures_restantes > 0:
                    cout_temps += vehicule.cost_for_next8hours * (heures_restantes / 8)
                    heures_restantes = 0
            else:
                cout_temps += vehicule.cost_for_first_8hours * (heures_restantes / 8)
                heures_restantes = 0

        cout_distance = distance_totale_km * vehicule.cost_per_km
        cout_fixe = getattr(vehicule, "cost_per_day", 0)
        cout_total = cout_temps + cout_distance + cout_fixe
        nb_jours = math.ceil(heures_facturees / 24)

        return nb_jours, cout_total

    else:
        km_par_jour = vehicule.average_speed * 24
        nb_jours = math.ceil(distance_totale_km / km_par_jour)
        cout_temps = nb_jours * vehicule.cost_per_day
        cout_distance = distance_totale_km * vehicule.cost_per_km
        cout_total = cout_temps + cout_distance
        return nb_jours, cout_total

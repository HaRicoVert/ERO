import random

import contextily
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx
import osmnx
from matplotlib.lines import Line2D

from common.utils import MIN_SNOW_LEVEL, MAX_SNOW_LEVEL


def connect_sectors(sectors_graph, montreal_graph):
    """
    Connecte les composantes non connexes du graphe des secteurs
    en utilisant les routes du graphe de Montréal
    """
    # Projeter le graphe de Montréal
    montreal_projected = osmnx.project_graph(montreal_graph)

    # Trouver les composantes faiblement connexes (pour graphes dirigés)
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
                # Si pas de chemin, connexion directe
                sectors_graph.add_edge(node1, node2, length=min_dist, snow_level=0)

    return sectors_graph


def generate_random_snow_levels(graph, min_level=0, max_level=15):
    for u, v, k, data in graph.edges(keys=True, data=True):
        data["snow_level"] = random.uniform(min_level, max_level)


def get_edge_colors(graph, color, min_snow_level, max_snow_level):
    colors = []
    black_color = (0, 0, 0, 1.0)

    for u, v, k, data in graph.edges(keys=True, data=True):
        snow_level = data["snow_level"]
        if snow_level < min_snow_level or snow_level > max_snow_level:
            colors.append(black_color)
        else:
            colors.append(
                color((snow_level - min_snow_level) / (max_snow_level - min_snow_level))
            )
    return colors


red_flash = mcolors.LinearSegmentedColormap.from_list(
    "red_flash",
    [(0.3, 0, 0), (1, 0, 0)],
    N=256,
)

blue = mcolors.LinearSegmentedColormap.from_list(
    "blue",
    [(0, 0, 0.5), (0, 0, 1)],
    N=256,
)

green_neon = mcolors.LinearSegmentedColormap.from_list(
    "green_neon",
    [(0, 0.5, 0), (0.2, 1, 0.2)],
    N=256,
)

colors = [red_flash, blue, green_neon]


def generate_plot_snow_level(graph, colormap):
    fig, ax = plt.subplots(figsize=(60, 60), dpi=100)

    # D'abord tracer le graphe
    edge_colors = get_edge_colors(graph, colormap, MIN_SNOW_LEVEL, MAX_SNOW_LEVEL)
    osmnx.plot_graph(
        graph,
        ax=ax,
        edge_color=edge_colors,
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

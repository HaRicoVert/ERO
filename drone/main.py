import networkx
import osmnx
from matplotlib import pyplot as plt

from drone.utils import (
    generate_random_snow_levels,
    blue,
    generate_plot_snow_level,
    connect_sectors,
)


def generate_graph():
    print("Chargement du graphe de Montreal sans les banlieues")
    montreal_graph = osmnx.graph_from_place(
        "Montreal, Quebec, Canada", network_type="drive"
    )
    sectors = [
        "Outremont, Montreal, Quebec, Canada",
        "Verdun, Montreal, Quebec, Canada",
        "Anjou, Montreal, Quebec, Canada",
        "Rivière-des-Prairies–Pointe-aux-Trembles, Montreal, Quebec, Canada",
        "Le Plateau-Mont-Royal, Montreal, Quebec, Canada",
    ]

    sectors_graphs = {}
    print("Chargement des secteurs")
    for sector in sectors:
        sectors_graphs[sector] = osmnx.graph_from_place(sector, network_type="drive")

    print("Projection des graphes de secteurs")
    projected_sectors = {}
    for sector, graph in sectors_graphs.items():
        projected_sectors[sector] = osmnx.project_graph(graph)

    print("Fusion des secteurs")
    sectors_combined = networkx.compose_all(list(projected_sectors.values()))
    first_graph = list(projected_sectors.values())[0]
    sectors_combined.graph.update(first_graph.graph)

    print("Génération des niveaux de neige aléatoires pour les secteurs")
    generate_random_snow_levels(sectors_combined, 0, 15)

    print("Simplification du graphe")
    return osmnx.consolidate_intersections(
        connect_sectors(sectors_combined, montreal_graph),
        tolerance=15,
        rebuild_graph=True,
    )


if __name__ == "__main__":
    graph = generate_graph()
    generate_plot_snow_level(graph, blue)
    plt.show()

    print(f"Taille: {graph.number_of_nodes()} nœuds, {graph.number_of_edges()} arêtes")
    print(
        f"Nombre d'arrêtes avec neige: {sum(1 for _, _, data in graph.edges(data=True) if 15 >= data['snow_level'] >= 2.5)}"
    )

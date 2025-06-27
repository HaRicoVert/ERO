import networkx
import osmnx

from drone.utils import (
    show_plot_before_scan,
    afficher_chemin,
    parcours_euler,
    generate_random_snow_levels,
    generate_plot_snow_level,
    blue,
    connect_sectors,
)


def generate_graph():
    print("Chargement du graphe de Montreal sans les banlieues")
    montreal_graph = osmnx.graph_from_place(
        "Montreal, Quebec, Canada", network_type="drive", simplify=False
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
        sectors_graphs[sector] = osmnx.graph_from_place(
            sector, network_type="drive", simplify=False
        )

    print("Projection des graphes de secteurs")
    projected_sectors = {}
    for sector, graph in sectors_graphs.items():
        projected_sectors[sector] = osmnx.project_graph(graph)

    print("Fusion des secteurs")
    sectors_combined = networkx.compose_all(list(projected_sectors.values()))
    first_graph = list(projected_sectors.values())[0]
    sectors_combined.graph.update(first_graph.graph)

    print("Simplification du graphe")
    graph = osmnx.consolidate_intersections(
        connect_sectors(sectors_combined, montreal_graph),
        tolerance=15,
        rebuild_graph=True,
    )

    return osmnx.simplify_graph(graph)


if __name__ == "__main__":
    graph = generate_graph()
    show_plot_before_scan(graph)
    afficher_chemin(graph, parcours_euler(graph))
    generate_random_snow_levels(graph)
    generate_plot_snow_level(graph, blue)

import networkx
import osmnx

from common.utils import blue, SUPER_DRONE
from drone.utils import (
    show_plot_before_scan,
    afficher_chemin,
    parcours_euler,
    generate_random_snow_levels,
    generate_plot_snow_level,
    calcul_cout,
)


def generate_graph():
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

    print("Simplification du graphe")
    return osmnx.consolidate_intersections(
        sectors_combined,
        tolerance=15,
        rebuild_graph=True,
    )


graph = generate_graph()
graph = generate_random_snow_levels(graph)
distance = sum(data["length"] for u, v, data in graph.edges(data=True))
distance = distance / 1000
print(f"Taille du réseau routier {distance:.2f} km")
nb_jours, cout_total = calcul_cout(
    SUPER_DRONE,
    distance,
)

print(f"Coût total du drone : {cout_total:.2f} € pour {nb_jours:.2f} jours")

if __name__ == "__main__":
    show_plot_before_scan(graph)
    afficher_chemin(graph, parcours_euler(graph))
    generate_plot_snow_level(graph, blue)

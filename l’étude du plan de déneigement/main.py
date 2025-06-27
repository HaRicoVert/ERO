import networkx
import osmnx
from matplotlib import pyplot as plt

from utilities.utils import (
    set_legend,
    blue,
    generate_random_snow_levels,
)

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


graph = connect_sectors(sectors_combined, montreal_graph)

print("Simplification du graphe")
graph = osmnx.consolidate_intersections(graph, tolerance=15, rebuild_graph=True)

set_legend(graph, blue)
# graphs = [graph, graph.copy(), graph.copy()]
# generate_legend([graph], [red_flash])
plt.show()

print(f"Taille: {graph.number_of_nodes()} nœuds, {graph.number_of_edges()} arêtes")
print(
    f"Nombre d'arrêtes avec neige: {sum(1 for _, _, data in graph.edges(data=True) if data['snow_level'] > 0)}"
)

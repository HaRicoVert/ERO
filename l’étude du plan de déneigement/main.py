import matplotlib.pyplot as plt
import networkx
import osmnx

from utilities.utils import (
    set_legend,
    generate_random_snow_levels,
)

sectors_to_exclude = [
    "Outremont, Montreal, Quebec, Canada",
    "Verdun, Montreal, Quebec, Canada",
    "Anjou, Montreal, Quebec, Canada",
    "Rivière-des-Prairies–Pointe-aux-Trembles, Montreal, Quebec, Canada",
    "Le Plateau-Mont-Royal, Montreal, Quebec, Canada",
]

# Récupérer le graphe complet de Montreal
montreal_graph = osmnx.graph_from_place(
    "Montreal, Quebec, Canada", network_type="drive"
)

# Récupérer les graphes des secteurs à exclure
sectors_graphs = {}
for sector in sectors_to_exclude:
    sectors_graphs[sector] = osmnx.graph_from_place(sector, network_type="drive")

# Combiner tous les graphes des secteurs à exclure
sectors_combined = networkx.compose_all(list(sectors_graphs.values()))


# Créer une copie du graphe de Montreal
montreal_filtered = montreal_graph.copy()

# Retirer les nœuds des secteurs spécifiés du graphe de Montreal
nodes_to_remove = set(sectors_combined.nodes()) & set(montreal_filtered.nodes())
montreal_filtered.remove_nodes_from(nodes_to_remove)

# On met snow_level à 0 pour les arêtes du graphe filtré
for u, v, k, data in montreal_filtered.edges(keys=True, data=True):
    data["snow_level"] = 0

generate_random_snow_levels(sectors_combined, min_level=0, max_level=15)

graph = networkx.compose(sectors_combined, montreal_filtered)

# Projeter et consolider le graphe filtré
graph = osmnx.project_graph(graph)
graph = osmnx.consolidate_intersections(graph, tolerance=20)
set_legend(plt, graph)
plt.show()

import matplotlib.pyplot as plt
import networkx
import osmnx

from utilities.utils import (
    generate_random_snow_levels,
    generate_legend,
    colors,
)

sectors = [
    "Outremont, Montreal, Quebec, Canada",
    "Verdun, Montreal, Quebec, Canada",
    "Anjou, Montreal, Quebec, Canada",
    "Rivière-des-Prairies–Pointe-aux-Trembles, Montreal, Quebec, Canada",
    "Le Plateau-Mont-Royal, Montreal, Quebec, Canada",
]

# Graphe complet de Montreal sans les banlieues
montreal_graph = osmnx.graph_from_place(
    "Montreal, Quebec, Canada", network_type="drive"
)

sectors_graphs = {}
for sector in sectors:
    sectors_graphs[sector] = osmnx.graph_from_place(sector, network_type="drive")

# On forme un seul graphe
sectors_combined = networkx.compose_all(list(sectors_graphs.values()))

# On retire les nœuds des secteurs du graphe de Montreal
montreal_without_sector = montreal_graph.copy()

# On retire les nœuds des secteurs du graphe de Montreal
montreal_without_sector.remove_nodes_from(sectors_combined.nodes())

# On met snow_level à 0 pour le graphe de Montreal sans les secteurs, pour pas que la déneigeuse ne s'occupe pas de
# ces routes
for u, v, k, data in montreal_without_sector.edges(keys=True, data=True):
    data["snow_level"] = 0

# On génère des niveaux de neige aléatoires pour les secteurs de l'énoncé
generate_random_snow_levels(sectors_combined, min_level=0, max_level=15)

# On combine les deux graphes
final_graph = networkx.compose(sectors_combined, montreal_without_sector)

# On convertit le graphe en un graphe projeté pour l'affichage et les calculs
graph = osmnx.project_graph(final_graph)
# On simplifie le graphe pour éviter les intersections inutiles
graph = osmnx.consolidate_intersections(graph, tolerance=15, rebuild_graph=True)
# set_legend(graph, blue)
graphs = [graph, graph.copy(), graph.copy()]
generate_legend(graphs, colors)
plt.show()

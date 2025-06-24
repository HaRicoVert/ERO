import matplotlib.pyplot as plt
import networkx
import osmnx

from utilities.utils import generate_random_snow_levels, set_legend

sectors = [
    "Outremont, Montreal, Quebec, Canada",
    "Verdun, Montreal, Quebec, Canada",
    "Anjou, Montreal, Quebec, Canada",
    "Rivière-des-Prairies–Pointe-aux-Trembles, Montreal, Quebec, Canada",
    "Le Plateau-Mont-Royal, Montreal, Quebec, Canada",
]

graphs = {}
for sector in sectors:
    graphs[sector] = osmnx.graph_from_place(sector, network_type="drive")

graph_list = list(graphs.values())
graph = networkx.compose_all(graph_list)
graph = osmnx.project_graph(graph)

graph = osmnx.consolidate_intersections(graph, tolerance=15)

generate_random_snow_levels(graph, min_level=0, max_level=15)
set_legend(plt, graph)
plt.show()

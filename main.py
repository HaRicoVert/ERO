import osmnx as ox
import networkx as nx
from itertools import combinations

#Drone:
#- 100 euro / jour
#- 0.01 euro / km

# Montreal graph roads
G = ox.graph.graph_from_place("Montreal, Quebec, Canada", network_type="drive")

# On converti le graph en undirected pour y appliquer l'algo chinese postman
G = G.to_undirected()

degrees = G.degree()

odd_nodes = []
for node, degree in degrees:
	if degree % 2 != 0:
		odd_nodes.append(node)


odd_G = nx.MultiDiGraph()

shortest_paths = nx.all_pairs_dijkstra_path_length(G, weight="length")

for u, v in combinations(odd_nodes, 2):
	distance = shortest_paths[u][v]
	odd_G.add_edge(u, v, weight=distance)

matching = nx.algorithms.matching.min_weight_matching(odd_G, maxcardinality=True, weight="weight")

for u, v in matching:
	path = nx.shortest_path(G, source=u, target=v, weight="length")
	for i in range(len(path) - 1):
		G.add_edge(path[i], path[i + 1], length=G[path[i]][path[i + 1]][0]['length'])

circuit = list(nx.eulerian_circuit(G))


ox.plot_graph(odd_G)

#for node, data in G.nodes(data=True):
#	print(f"Node {node}: {data}")

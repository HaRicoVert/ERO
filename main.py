import osmnx as ox
import networkx as nx

#Drone:
#- 100 euro / jour
#- 0.01 euro / km

# Montreal graph roads
G = ox.graph.graph_from_place("Montreal, Quebec, Canada", network_type="drive")

# On converti le graph en undirected pour y appliquer l'algo chinese postman
G = G.to_undirected()

degrees = G.degree()

odd_degrees = []
for node, degree in degrees:
	if degree % 2 != 0:
		odd_degrees.append(node)

odd_G = nx.MultiDiGraph()

dijkstra_result = nx.all_pairs_dijkstra_path_length(odd_G, weight="length")

jsp = 0


#ox.plot_graph(G)

for node, data in G.nodes(data=True):
	print(f"Node {node}: {data}")

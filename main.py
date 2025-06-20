import osmnx as ox

#Drone:
#- 100 euro / jour
#- 0.01 euro / km

# Montreal graph roads
G = ox.graph.graph_from_place("Montreal, Quebec, Canada", network_type="drive")

# On converti le graph en undirected pour y appliquer l'algo chinese postman
G_undirected = G.to_undirected()

#ox.plot_graph(G)

for node, data in G.nodes(data=True):
	print(f"Node {node}: {data}")

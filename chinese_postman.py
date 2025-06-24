import os
import networkx
import networkx as nx
import pickle

"""
Retourne : 
	List: Une liste de nodes representant le trajet Eulerien commencant a start_node.
	Renvoi None si le graph n'a pas pu etre converti en Eulerien.
"""
def chinese_postman(G_directed: networkx.MultiDiGraph, start_node):
	G = G_directed.to_undirected()

	print("Step 1")
	# Identifier les sommets de degré impair
	odd_nodes = [node for node, degree in G.degree() if degree % 2 != 0]

	print("Step 2")
	# Calculer les distances minimales entre paires de sommets impairs
	shortest_paths_file = "shortest_paths.pkl"

	if not os.path.exists(shortest_paths_file):
		print("Calcul des plus courts chemins entre sommets impairs...")
		all_lengths = dict(nx.all_pairs_dijkstra_path_length(G, weight="length"))
		shortest_paths = {}
		for u in odd_nodes:
			for v in odd_nodes:
				if u != v and v in all_lengths[u]:
					if u not in shortest_paths:
						shortest_paths[u] = {}
					shortest_paths[u][v] = all_lengths[u][v]
		with open(shortest_paths_file, "wb") as f:
			pickle.dump(shortest_paths, f)
	else:
		print("Chargement des distances depuis cache...")
		with open(shortest_paths_file, "rb") as f:
			shortest_paths = pickle.load(f)

	print("Step 3")
	# Construire le graphe complet pondéré entre les sommets impairs
	odd_G = nx.Graph()
	for u in shortest_paths:
		for v in shortest_paths[u]:
			odd_G.add_edge(u, v, weight=shortest_paths[u][v])

	print("Step 4")
	# Calculer le matching parfait de poids minimal
	matching = nx.algorithms.matching.min_weight_matching(odd_G, weight="weight")

	print("Step 5")
	# Ajouter les chemins du matching dans le graphe original
	for u, v in matching:
		path = nx.shortest_path(G, source=u, target=v, weight="length")
		for i in range(len(path) - 1):
			u1, v1 = path[i], path[i + 1]
			edge_data = list(G[u1][v1].values())[0]
			G.add_edge(u1, v1, **edge_data)

	print("Step 6")
	# 8. Générer le circuit eulérien depuis la mairie
	if nx.is_eulerian(G):
		euler_circuit = list(nx.eulerian_circuit(G, source=start_node))
		euler_path = [u for u, v in euler_circuit] + [euler_circuit[-1][1]]
	else:
		print("Le graphe n'est pas eulérien.")
		euler_path = None

	return euler_path

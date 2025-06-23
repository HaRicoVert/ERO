import os
import osmnx as ox
import networkx as nx
import pickle
import numpy as np
from matplotlib import pyplot as plt

# ----------------------------
# Fonction pour dessiner des flèches régulièrement sur le chemin
# ----------------------------
def draw_arrows_on_path(G, path, ax, step=20, arrow_length=20, color="blue"):
	for i in range(0, len(path) - 1, step):
		u = path[i]
		v = path[i + 1]

		x1, y1 = G.nodes[u]['x'], G.nodes[u]['y']
		x2, y2 = G.nodes[v]['x'], G.nodes[v]['y']

		dx, dy = x2 - x1, y2 - y1
		norm = np.hypot(dx, dy)
		if norm == 0:
			continue

		dx, dy = dx / norm, dy / norm
		ax.arrow(x1, y1, dx * arrow_length, dy * arrow_length,
				 head_width=10, head_length=10, fc=color, ec=color, zorder=4)

# ----------------------------
# 1. Télécharger un graphe plus petit (quartier)
# ----------------------------
print("Step 1")
G_directed = ox.graph_from_place("Ville-Marie, Montreal, Quebec, Canada", network_type="drive")
G = G_directed.to_undirected()

print("Step 2")
# 2. Identifier les sommets de degré impair
odd_nodes = [node for node, degree in G.degree() if degree % 2 != 0]

print("Step 3")
# 3. Calculer les distances minimales entre paires de sommets impairs (avec cache)
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

print("Step 4")
# 4. Construire le graphe complet pondéré entre les sommets impairs
odd_G = nx.Graph()
for u in shortest_paths:
	for v in shortest_paths[u]:
		odd_G.add_edge(u, v, weight=shortest_paths[u][v])

print("Step 5")
# 5. Calculer le matching parfait de poids minimal
matching = nx.algorithms.matching.min_weight_matching(odd_G, weight="weight")

print("Step 6")
# 6. Ajouter les chemins du matching dans le graphe original
for u, v in matching:
	path = nx.shortest_path(G, source=u, target=v, weight="length")
	for i in range(len(path) - 1):
		u1, v1 = path[i], path[i + 1]
		edge_data = list(G[u1][v1].values())[0]
		G.add_edge(u1, v1, **edge_data)

print("Step 7")
# 7. Définir le point de départ à la Mairie de Montréal
lat, lon = ox.geocode("275 Rue Notre-Dame Est, Montréal, QC")
start_node = ox.distance.nearest_nodes(G_directed, lon, lat)

print("Step 8")
# 8. Générer le circuit eulérien depuis la mairie
if nx.is_eulerian(G):
	euler_circuit = list(nx.eulerian_circuit(G, source=start_node))
	euler_path = [u for u, v in euler_circuit] + [euler_circuit[-1][1]]
else:
	print("Le graphe n'est pas eulérien.")
	euler_path = None

# ----------------------------
# 9. Affichage du graphe avec flèches
# ----------------------------
print("Step 9 : Affichage")
fig, ax = ox.plot_graph(G, show=False, close=False)

if euler_path:
	ox.plot_graph_route(G, euler_path, route_linewidth=2, ax=ax, show=False, close=False)

# Marquer le point de départ
x, y = G.nodes[start_node]['x'], G.nodes[start_node]['y']
ax.scatter(x, y, c='yellow', s=80, marker='o', label='Départ : Mairie', zorder=5)

ax.legend()
plt.show()

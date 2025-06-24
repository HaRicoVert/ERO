import os
import random

import osmnx as ox
import networkx as nx
import pickle
import numpy as np
from matplotlib import pyplot as plt

# ----------------------------
# 1. Télécharger un graphe plus petit (quartier)
# ----------------------------
print("Step 1")
G_directed = ox.graph_from_place("Ville-Marie, Montreal, Quebec, Canada", network_type="drive")

for u, v, k, data in G_directed.edges(keys=True, data=True):
	# On ajoute la neige
	cm_neige = random.randint(0, 15)
	data["cm_neige"] = cm_neige

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


import contextily as ctx

# Définir les couleurs d’arêtes selon la neige
edge_colors = []
for u, v, data in G.edges(data=True):
	neige = data.get("cm_neige", 0)
	if 2.5 <= neige <= 15:
		edge_colors.append("red")
	else:
		edge_colors.append("blue")

# Convertir le graphe en GeoDataFrame pour le fond OSM
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

# Tracer sans fond
fig, ax = ox.plot_graph(G, edge_color=edge_colors, edge_linewidth=1.5, node_size=0, show=False, close=False)

# Ajouter le fond cartographique (OpenStreetMap via contextily)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=gdf_edges.crs.to_string())

# Marquer le point de départ
x, y = G.nodes[start_node]['x'], G.nodes[start_node]['y']
ax.scatter(x, y, c='yellow', s=80, marker='o', label='Départ : Mairie', zorder=5)

ax.legend()
plt.tight_layout()
plt.show()

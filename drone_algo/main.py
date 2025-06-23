import osmnx as ox
import networkx as nx

from matplotlib import pyplot as plt

# 1. Télécharger le graphe routier de Montréal
G_directed = ox.graph_from_place("Montreal, Quebec, Canada", network_type="drive", retain_all=True)
G = G_directed.to_undirected()

print("Step 2")
# 2. Identifier les sommets de degré impair
odd_nodes = [node for node, degree in G.degree() if degree % 2 != 0]

print("Step 3")
# 3. Calculer les distances minimales entre chaque paire de sommets impairs
shortest_paths = {}
for u in odd_nodes:
	lengths = nx.single_source_dijkstra_path_length(G, u, weight="length")
	for v in odd_nodes:
		if u != v and v in lengths:
			if u not in shortest_paths:
				shortest_paths[u] = {}
			shortest_paths[u][v] = lengths[v]

print("Step 4")
# 4. Construire le graphe complet entre les sommets impairs
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
		# Utiliser la première arête existante entre u1 et v1
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
	ox.plot_graph_route(G, euler_path, route_linewidth=4)
else:
	print("Le graphe n'est pas eulérien.")
	euler_path = None

fig, ax = ox.plot_graph(G, show=False, close=False)

# Tracer le circuit si disponible
if euler_path:
	ox.plot_graph_route(G, euler_path, route_linewidth=2, ax=ax, show=False, close=False)

# 6. Marquer le point de départ (la mairie)
x, y = G.nodes[start_node]['x'], G.nodes[start_node]['y']
ax.scatter(x, y, c='yellow', s=80, marker='o', label='Départ : Mairie', zorder=5)

# 7. Afficher la légende et la carte
ax.legend()
plt.show()

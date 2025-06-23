import osmnx as ox
import networkx as nx
from itertools import combinations
import contextily as ctx
from shapely.geometry import Point, LineString
import geopandas as gpd

from matplotlib import pyplot as plt

# 1. Télécharger le graphe routier de Montréal
G_directed = ox.graph_from_place("Plateau Mont-Royal, Montreal, Quebec, Canada", network_type="drive")
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

# grab the x/y for every node in the route
route_xy   = [(G.nodes[n]['x'], G.nodes[n]['y']) for n in euler_path]
route_line = LineString(route_xy)

# point for the start
start_pt   = Point(lon, lat)

# GeoDataFrames in WGS84
gdf_route = gpd.GeoDataFrame(
	{'geometry': [route_line]},
	crs="EPSG:4326"
)
gdf_start = gpd.GeoDataFrame(
	{'geometry': [start_pt]},
	crs="EPSG:4326"
)

# reproject to Web Mercator
gdf_route = gdf_route.to_crs(epsg=3857)
gdf_start = gdf_start.to_crs(epsg=3857)

# ——————————————————————————————————————————————
# 3) (Optional) also pull in all the graph’s edges as a backdrop
#    for a bit of street fuzz behind your highlight
nodes, edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
edges = edges.to_crs(epsg=3857)

# ——————————————————————————————————————————————
# 4) Plot everything over a tile basemap

fig, ax = plt.subplots(figsize=(10, 10))

# light grey background streets
edges.plot(ax=ax, linewidth=0.5, edgecolor="#aaaaaa", zorder=1)

# your Eulerian tour, thicker & brighter
gdf_route.plot(
	ax=ax,
	linewidth=3,
	alpha=0.9,
	color="royalblue",
	zorder=3,
	label="Circuit eulérien"
)

# start marker
gdf_start.plot(
	ax=ax,
	marker="*",
	markersize=100,
	color="crimson",
	zorder=4,
	label="Départ : Mairie"
)

# add the web tiles underneath
ctx.add_basemap(
	ax,
	source=ctx.providers.CartoDB.Positron,  # or Stamen.Terrain, Stamen.TonerLite, etc.
	zoom=14
)

ax.axis("off")
ax.legend(frameon=True, loc="lower left")
plt.tight_layout()
plt.show()

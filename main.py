import random

import osmnx

import graph
from algo import chinese_postman

G_directed = osmnx.graph_from_place(
    "Ville-Marie, Montreal, Quebec, Canada", network_type="drive"
)

# Définir le point de départ à la Mairie de Montréal
lat, lon = osmnx.geocode("275 Rue Notre-Dame Est, Montréal, QC")
start_node = osmnx.distance.nearest_nodes(G_directed, lon, lat)

graph.visualize_snow_level(G_directed, start_node)

# On ajoute une quantite de neige aleatoire (de 0 a 15) sur les arretes du graph
for u, v, k, data in G_directed.edges(keys=True, data=True):
    cm_neige = random.randint(0, 15)
    data["cm_neige"] = cm_neige

drone_path = chinese_postman(G_directed, start_node)
graph.visualize_euler_path_with_arrows(G_directed, drone_path, start_node)
graph.visualize_snow_level(G_directed, start_node)

import contextily as ctx
import matplotlib.pyplot as plt
import osmnx as ox


def visualize_snow_level(G, start_node):
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
    fig, ax = ox.plot_graph(
        G,
        edge_color=edge_colors,
        edge_linewidth=1.5,
        node_size=0,
        show=False,
        close=False,
    )

    # Ajouter le fond cartographique (OpenStreetMap via contextily)
    ctx.add_basemap(
        ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=gdf_edges.crs.to_string()
    )

    # Marquer le point de départ
    x, y = G.nodes[start_node]["x"], G.nodes[start_node]["y"]
    ax.scatter(x, y, c="yellow", s=80, marker="o", label="Départ : Mairie", zorder=5)

    ax.legend()
    plt.tight_layout()
    plt.show()


def visualize_euler_path_with_arrows(G, euler_path, start_node, step=20):
    import contextily as ctx
    import matplotlib.pyplot as plt
    import geopandas as gpd
    from shapely.geometry import Point, LineString

    # Convertir tous les points en WGS84
    coords = [(G.nodes[n]["x"], G.nodes[n]["y"]) for n in euler_path if n in G.nodes]
    gdf_line = gpd.GeoDataFrame(geometry=[LineString(coords)], crs="EPSG:4326").to_crs(
        epsg=3857
    )

    # Créer les flèches tous les X segments
    arrow_lines = []
    for i in range(0, len(coords) - 1, step):
        x1, y1 = coords[i]
        x2, y2 = coords[i + 1]
        arrow_lines.append(((x1, y1), (x2, y2)))
    arrow_gdf = gpd.GeoDataFrame(
        geometry=[LineString([a, b]) for a, b in arrow_lines], crs="EPSG:4326"
    ).to_crs(epsg=3857)

    # Préparer figure
    fig, ax = plt.subplots(figsize=(12, 12))

    # Tracer ligne complète
    gdf_line.plot(ax=ax, linewidth=1.8, color="green", zorder=2)

    # Tracer flèches espacées
    for line in arrow_gdf.geometry:
        x1, y1 = line.coords[0]
        x2, y2 = line.coords[1]
        ax.annotate(
            "",
            xy=(x2, y2),
            xycoords="data",
            xytext=(x1, y1),
            textcoords="data",
            arrowprops=dict(arrowstyle="->", color="black", lw=1),
            zorder=3,
        )

    pt = Point(G.nodes[start_node]["x"], G.nodes[start_node]["y"])
    start_point = gpd.GeoSeries([pt], crs="EPSG:4326").to_crs(epsg=3857)
    start_point.plot(
        ax=ax, color="yellow", markersize=80, zorder=4, label="Départ : Mairie"
    )

    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs="EPSG:3857")

    ax.set_title("Trajet du drone")
    ax.legend()
    plt.tight_layout()
    plt.show()

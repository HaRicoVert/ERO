if __name__ == "__main__":
    import osmnx as ox
    import matplotlib.pyplot as plt
    import contextily

    sectors = [
        "Outremont, Montreal, Quebec, Canada",
        "Verdun, Montreal, Quebec, Canada",
        "Anjou, Montreal, Quebec, Canada",
        "Rivière-des-Prairies–Pointe-aux-Trembles, Montreal, Quebec, Canada",
        "Le Plateau-Mont-Royal, Montreal, Quebec, Canada",
    ]

    montreal_boundary = ox.geocode_to_gdf("Montreal, Quebec, Canada")
    highlighted_gdf = []

    for sector in sectors:
        try:
            gdf = ox.geocode_to_gdf(sector)
            highlighted_gdf.append(gdf)
        except:
            continue

    fig, ax = plt.subplots(figsize=(15, 15))

    colors = ["red", "blue", "green", "orange", "purple"]
    for i, gdf in enumerate(highlighted_gdf):
        gdf.plot(ax=ax, color=colors[i], alpha=0.5, edgecolor=colors[i], linewidth=3)

    contextily.add_basemap(
        ax,
        crs=montreal_boundary.crs,
        source=contextily.providers.OpenStreetMap.Mapnik,
        alpha=0.8,
    )

    plt.title(
        "Secteur à déneiger de Montréal sans les banlieues",
        fontsize=16,
        fontweight="bold",
    )
    plt.axis("off")
    plt.tight_layout()
    plt.show()

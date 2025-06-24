from random import randint

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import osmnx
from matplotlib.cm import ScalarMappable
from matplotlib.lines import Line2D

# multi_query = [
#     "Outremont",
#     "Verdun",
#     "Anjou",
#     "Rivière-des-Prairies–Pointe-aux-Trembles",
#     "Le Plateau-Mont-Royal",
# ]
#
# graphe_outremont = osmnx.graph_from_place(multi_query, network_type="drive")

# Charger le graphe
graphe_outremont = osmnx.graph_from_place(
    "Outremont, Montreal, Quebec, Canada", network_type="drive"
)


# Ajouter les niveaux de neige
for u, v, k, data in graphe_outremont.edges(keys=True, data=True):
    data["snow_level"] = randint(0, 15)


def get_edge_colors(G):
    colors = []
    gray_color = (1, 1, 1, 1.0)  # RGBA pour blanc

    green_yellow = mcolors.LinearSegmentedColormap.from_list(
        "green_yellow", ["green", "yellow"]
    )

    for u, v, k, data in G.edges(keys=True, data=True):
        snow_level = data["snow_level"]
        if snow_level < 2.5 or snow_level > 15:
            colors.append(gray_color)
        else:
            normalized = (snow_level - 2.5) / (15 - 2.5)
            colors.append(green_yellow(normalized))
    return colors


fig, ax = plt.subplots(figsize=(12, 8))

edge_colors = get_edge_colors(graphe_outremont)
osmnx.plot_graph(
    graphe_outremont,
    ax=ax,
    edge_color=edge_colors,
    edge_linewidth=3,
    node_size=0,
    show=False,
    close=False,
)

# Créer la légende avec gradient
# Colorbar pour la zone d'intérêt (2.5-15 cm)
norm = mcolors.Normalize(vmin=2.5, vmax=15)
sm = ScalarMappable(norm=norm, cmap=plt.cm.Greens)
sm.set_array([])

cbar = plt.colorbar(sm, ax=ax, shrink=0.8, aspect=20)
cbar.set_label("Niveau de neige (cm)", rotation=270, labelpad=20)

legend_elements = [
    Line2D(
        [0], [0], color="gray", lw=3, label="< 2.5 cm ou > 15 cm (pas de déneigement)"
    ),
    Line2D(
        [0], [0], color=plt.cm.Greens(0.3), lw=3, label="2.5 cm (déneigement requis)"
    ),
    Line2D(
        [0], [0], color=plt.cm.Greens(1.0), lw=3, label="15 cm (déneigement requis)"
    ),
]

ax.legend(handles=legend_elements, loc="upper right", bbox_to_anchor=(1, 1))

plt.title("Réseau routier d'Outremont - Niveaux de neige")
plt.tight_layout()
plt.show()

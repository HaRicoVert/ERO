import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import osmnx
from matplotlib.cm import ScalarMappable
from matplotlib.lines import Line2D

from utilities.utils import generate_random_snow_levels, MIN_SNOW_LEVEL, MAX_SNOW_LEVEL
from utilities.utils import get_edge_colors

# multi_query = [
#     "Outremont",
#     "Verdun",
#     "Anjou",
#     "Rivière-des-Prairies–Pointe-aux-Trembles",
#     "Le Plateau-Mont-Royal",
# ]
#
# graphe_outremont = osmnx.graph_from_place(multi_query, network_type="drive")

graph = osmnx.graph_from_place(
    "Outremont, Montreal, Quebec, Canada", network_type="drive"
)

generate_random_snow_levels(graph, min_level=0, max_level=15)

fig, ax = plt.subplots(figsize=(12, 8))
edge_colors = get_edge_colors(graph)
osmnx.plot_graph(
    graph,
    ax=ax,
    edge_color=edge_colors,
    edge_linewidth=3,
    node_size=0,
    show=False,
    close=False,
)

sm = ScalarMappable(
    norm=mcolors.Normalize(vmin=MIN_SNOW_LEVEL, vmax=MAX_SNOW_LEVEL), cmap=plt.cm.Greens
)
sm.set_array([])

cbar = plt.colorbar(sm, ax=ax, shrink=0.8, aspect=20)
cbar.set_label("Niveau de neige (cm)", rotation=270, labelpad=20)

legend_elements = [
    Line2D(
        [0],
        [0],
        color="gray",
        lw=3,
        label=f"< {MIN_SNOW_LEVEL} cm ou > {MAX_SNOW_LEVEL} cm (pas de déneigement)",
    ),
    Line2D(
        [0],
        [0],
        color=plt.cm.Greens(0.3),
        lw=3,
        label=f"{MIN_SNOW_LEVEL} cm (déneigement requis)",
    ),
    Line2D(
        [0],
        [0],
        color=plt.cm.Greens(1.0),
        lw=3,
        label=f"{MAX_SNOW_LEVEL} cm (déneigement requis)",
    ),
]

ax.legend(handles=legend_elements, loc="upper right", bbox_to_anchor=(1, 1))

plt.title("Réseau routier d'Outremont - Niveaux de neige")
plt.show()

import os

import networkx
from dotenv import load_dotenv
from matplotlib import colors as mcolors


class Vehicule:
    def __init__(self, cost_per_day, cost_per_km):
        self.cost_per_day = cost_per_day
        self.cost_per_km = cost_per_km
        self.average_speed = 0

    def __str__(self):
        return f"Vehicule(cost={self.cost_per_day}, cost_per_km={self.cost_per_km})"


class SuperDrone(Vehicule):
    def __init__(self, cost_per_day, cost_per_km):
        super().__init__(cost_per_day, cost_per_km)
        self.average_speed = 60

    def __str__(self):
        return f"SuperDrone(cost={self.cost_per_day}, cost_per_km={self.cost_per_km})"


class Snowplow(Vehicule):
    def __init__(
        self,
        cost_per_day,
        cost_per_km,
        cost_for_first_8hours,
        cost_for_next8hours,
        average_speed,
    ):
        super().__init__(cost_per_day, cost_per_km)
        self.cost_for_first_8hours = cost_for_first_8hours
        self.cost_for_next8hours = cost_for_next8hours
        self.average_speed = average_speed

    def __str__(self):
        return f"Snowplow(cost={self.cost_per_day}, cost_per_km={self.cost_per_km}, cost_for_first_8hours={self.cost_for_first_8hours}, cost_for_next8hours={self.cost_for_next8hours}, average_speed={self.average_speed})"


load_dotenv("../.env")


SUPER_DRONE = SuperDrone(
    cost_per_day=float(os.getenv("DRONE_COST_PER_DAY")),
    cost_per_km=float(os.getenv("DRONE_COST_PER_KM")),
)

SNOWPLOW_TYPE_1 = Snowplow(
    cost_per_day=float(os.getenv("SNOWPLOW_TYPE1_COST_PER_DAY")),
    cost_per_km=float(os.getenv("SNOWPLOW_TYPE1_COST_PER_KM")),
    cost_for_first_8hours=float(os.getenv("SNOWPLOW_TYPE1_COST_FOR_FIRST_8_HOURS")),
    cost_for_next8hours=float(os.getenv("SNOWPLOW_TYPE1_COST_FOR_NEXT_8_HOURS")),
    average_speed=float(os.getenv("SNOWPLOW_TYPE1_AVERAGE_SPEED")),
)

SNOWPLOW_TYPE_2 = Snowplow(
    cost_per_day=float(os.getenv("SNOWPLOW_TYPE2_COST_PER_DAY")),
    cost_per_km=float(os.getenv("SNOWPLOW_TYPE2_COST_PER_KM")),
    cost_for_first_8hours=float(os.getenv("SNOWPLOW_TYPE2_COST_FOR_FIRST_8_HOURS")),
    cost_for_next8hours=float(os.getenv("SNOWPLOW_TYPE2_COST_FOR_NEXT_8_HOURS")),
    average_speed=float(os.getenv("SNOWPLOW_TYPE2_AVERAGE_SPEED")),
)

MIN_SNOW_LEVEL = float(os.getenv("MIN_SNOW_LEVEL"))
MAX_SNOW_LEVEL = float(os.getenv("MAX_SNOW_LEVEL"))

red_flash = mcolors.LinearSegmentedColormap.from_list(
    "red_flash",
    [(0.3, 0, 0), (1, 0, 0)],
    N=256,
)

blue = mcolors.LinearSegmentedColormap.from_list(
    "blue",
    [(0, 0, 0.5), (0, 0, 1)],
    N=256,
)

green = mcolors.LinearSegmentedColormap.from_list(
    "green",
    [(0, 0.5, 0), (0.2, 1, 0.2)],
    N=256,
)

purple = mcolors.LinearSegmentedColormap.from_list(
    "purple",
    [(0.3, 0, 0.5), (0.8, 0.2, 1)],
    N=256,
)

orange = mcolors.LinearSegmentedColormap.from_list(
    "orange",
    [(0.5, 0.2, 0), (1, 0.6, 0)],
    N=256,
)

colors = [red_flash, blue, green, purple, orange]


def split_graph(graph):
    components = networkx.connected_components(graph.to_undirected())
    return [graph.subgraph(comp).copy() for comp in components]

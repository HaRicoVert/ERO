import os
import random

import matplotlib.colors as mcolors
from dotenv import load_dotenv


class Vehicule:
    def __init__(self, cost_per_day, cost_per_km):
        self.cost_per_day = cost_per_day
        self.cost_per_km = cost_per_km

    def __str__(self):
        return f"Vehicule(cost={self.cost_per_day}, cost_per_km={self.cost_per_km})"


class SuperDrone(Vehicule):
    def __init__(self, cost_per_day, cost_per_km):
        super().__init__(cost_per_day, cost_per_km)

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


def generate_random_snow_levels(graph, min_level=0, max_level=15):
    for u, v, k, data in graph.edges(keys=True, data=True):
        data["snow_level"] = random.uniform(min_level, max_level)


def get_edge_colors(graph):
    colors = []
    black_color = (0, 0, 0, 1.0)

    green_yellow = mcolors.LinearSegmentedColormap.from_list(
        "green_yellow", ["green", "yellow"]
    )

    for u, v, k, data in graph.edges(keys=True, data=True):
        snow_level = data["snow_level"]
        if snow_level < MIN_SNOW_LEVEL or snow_level > MAX_SNOW_LEVEL:
            colors.append(black_color)
        else:
            colors.append(
                green_yellow(
                    (snow_level - MIN_SNOW_LEVEL) / (MAX_SNOW_LEVEL - MIN_SNOW_LEVEL)
                )
            )
    return colors

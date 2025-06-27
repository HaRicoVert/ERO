import os

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

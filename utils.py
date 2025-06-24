class Vehicule:
    def __init__(self, cost, cost_per_km):
        self.cost = cost
        self.cost_per_km = cost_per_km

    def __str__(self):
        return f"Vehicule(cost={self.cost}, cost_per_km={self.cost_per_km})"


class Drone(Vehicule):
    def __init__(self, cost, cost_per_km):
        super().__init__(cost, cost_per_km)

    def __str__(self):
        return f"Drone(cost={self.cost}, cost_per_km={self.cost_per_km})"


class Snowplow(Vehicule):
    def __init__(
        self,
        cost,
        cost_per_km,
        cost_for_first_8hours,
        cost_for_next8hours,
        average_speed,
    ):
        super().__init__(cost, cost_per_km)
        self.cost_for_first_8hours = cost_for_first_8hours
        self.cost_for_next8hours = cost_for_next8hours
        self.average_speed = average_speed

    def __str__(self):
        return f"Snowplow(cost={self.cost}, cost_per_km={self.cost_per_km}, cost_for_first_8hours={self.cost_for_first_8hours}, cost_for_next8hours={self.cost_for_next8hours}, average_speed={self.average_speed})"

from math import ceil

from drawable_objects.planet import Planet
from geometry.distances import dist


class TravelCostCounter:
    """
    Счетчик стоимости перелета между планетами.
    """
    def __init__(self):
        pass

    def get_cost(self, planet_from: Planet, planet_to: Planet) -> int:
        travel_length = dist(planet_from.estimated_pos, planet_to.estimated_pos)
        return ceil(travel_length / 2.5)

from math import ceil

from drawable_objects.planet import Planet
from geometry.vector import length


class TravelCostCounter:
    """
    Счетчик стоимости перелета между планетами.
    """
    HORIZONTAL_KOEF = 0.6
    VERTICAL_KOEF = 0.4
    
    def __init__(self):
        pass

    def get_cost(self, planet_from: Planet, planet_to: Planet) -> int:
        travel_vector = planet_to.estimated_pos - planet_from.estimated_pos
        travel_vector.x *= self.HORIZONTAL_KOEF
        travel_vector.y *= self.VERTICAL_KOEF
        return ceil(length(travel_vector))

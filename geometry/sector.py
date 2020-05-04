"""
Сектор круга
"""
from geometry.optimized.segment import get_vector
from geometry.point import Point
from geometry.vector import cross_product, length, vector_from_length_angle
from pygame import draw
from geometry.vector import sign

class Sector:
    """
    Сектора круга
    """
    def __init__(self, radius: float, center: Point, rotation_angle: float, arc_angle: float):
        self.__center = center
        self.__radius = radius
        self.__rotation_angle = rotation_angle #угол поворота сектора
        self.__arc_angle = arc_angle #сам угол сектора (дуга, на которую он опирается).

    def is_inside(self, p: Point) -> bool:
        """
        находится ли точка внутри сегмента
        """
        if length(self.__center - p) > self.__radius:
            return False

        mult1 = cross_product(get_vector(self.__center, p), get_vector(self.__center, self.__p1))
        if mult1 > 0:
            return False

        mult2 = cross_product(get_vector(self.__center, p), get_vector(self.__center, self.__p2))
        return mult2 >= 0

    @property
    def __p1(self) -> Point:
        """
        Получить первую крайнюю точку сегмента на окружности
        """
        return self.__center + vector_from_length_angle(self.__radius, self.__rotation_angle + self.__arc_angle / 2)

    @property
    def __p2(self) -> Point:
        """
        Получить вторую крайнюю точку сегмента на окружности
        """
        return self.__center + vector_from_length_angle(self.__radius, self.__rotation_angle - self.__arc_angle / 2)

    def process_draw(self, screen):
        """
        Отрисовка для debug
        """
        draw.line(screen, (0, 0, 255), [self.__center.x, self.__center.y], [self.__p1.x, self.__p1.y], 10)
        draw.line(screen, (0, 0, 255), [self.__center.x, self.__center.y], [self.__p2.x, self.__p2.y], 10)


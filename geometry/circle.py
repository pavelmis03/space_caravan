from geometry.point import Point
from geometry.vector import sign
from geometry.distances import dist


class Circle:
    """
    Класс геометрической окружности.

    :param center: центр
    :param r: радиус
    """

    def __init__(self, center: Point = Point(), r: float = 0):
        self.center = center
        self.r = r

    def is_inside(self, p: Point) -> bool:
        """
        Лежит ли точка внутри окружности.

        :param p: точка
        :return: логическое значение
        """
        return sign(dist(self.center, p) - self.r) != 1

from math import sqrt

from geometry.point import Point
from geometry.vector import sign


class Line:
    """
    Класс геометрической линии, заданной тремя коэффициентами уравенения ax + by + c = 0.

    :param a: коэффициент a
    :param b: коэффициент b
    :param c: коэффициент c
    """

    def __init__(self, a: float = 1, b: float = 1, c: float = 0):
        self.a = a
        self.b = b
        self.c = c

    def get_normal(self):
        """
        Вектор нормали к прямой.

        :return: соответствующий вектор
        """
        return Point(self.a, self.b)

    def get_parallel(self):
        """
        Вектор, параллельный прямой. Повернут на 90 градусов вправо относительно вектора нормали.

        :return: соответствующий вектор
        """
        return Point(self.b, -self.a)

    def __eq__(self, other):
        """ Overload == for tests """
        return self.a == other.a and self.b == other.b and self.c == other.c


def line_from_points(p1: Point, p2: Point) -> Line:
    """
    Линия, проходящая через две заданные точки.

    :param p1: первая точка
    :param p2: вторая точка
    :return: соответствующая линия
    """
    a = p2.y - p1.y
    b = p1.x - p2.x
    c = -a * p1.x - b * p1.y
    return Line(a, b, c)


def point_on_line(p: Point, l: Line) -> bool:
    """
    Проверка принадлежности точки прямой.

    :param p: точка для проверки
    :param l: прямая
    :return: логическое значение
    """
    return sign(l.a * p.x + l.b * p.y + l.c) == 0

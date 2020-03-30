from geometry.point import Point
from geometry.vector import cross_product, dot_product, sign, length


class Segment:
    """
    Класс геометрического отрезка, заданного двумя точками - концами, или началом и концом.

    :param p1: первый конец (начало)
    :param p2: второй конец (собственно конец)
    """
    def __init__(self, p1: Point = Point(), p2: Point = Point()):
        self.p1 = Point(p1.x, p1.y)
        self.p2 = Point(p2.x, p2.y)

    @property
    def length(self):
        return length(self.p1 - self.p2)


def point_on_segment(p: Point, seg: Segment) -> bool:
    """
    Проверка принадлежности точки отрезку.

    :param p: точка для проверки
    :param seg: отрезок
    :return: логическое значение
    """
    if sign(cross_product(p - seg.p1, seg.p2 - seg.p1)) != 0:
        return False
    return sign(dot_product(p - seg.p1, seg.p2 - seg.p1)) >= 0 and sign(dot_product(p - seg.p2, seg.p1 - seg.p2)) >= 0

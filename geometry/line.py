from geometry.point import Point
from geometry.vector import cross_product, sign
from constants import EPS


class Line:
    def __init__(self, a: float = 1, b: float = 1, c: float = 0):
        self.a = a
        self.b = b
        self.c = c

    def get_normal(self):
        return Point(self.a, self.b)


def line_from_points(p1: Point, p2: Point) -> Line:
    a = p2.y - p1.y
    b = p1.x - p2.x
    c = -a * p1.x - b * p1.y
    return Line(a, b, c)


def intersect_lines(l1: Line, l2: Line) -> Point:
    if sign(cross_product(l1.get_normal(), l2.get_normal())) == 0:
        return None
    x = (l1.b * l2.c - l2.b * l1.c) / (l1.a * l2.b - l2.a * l1.b)
    y = (l1.a * l2.c - l2.a * l1.c) / (l2.a * l1.b - l1.a * l2.b)
    return Point(x, y)

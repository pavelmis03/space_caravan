from math import sqrt

from geometry.point import Point
from geometry.vector import sign


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


def point_on_line(p: Point, l: Line):
    return sign(l.a * p.x + l.b * p.y + l.c) == 0


def dist_point_line(p: Point, l: Line) -> float:
    return abs(l.a * p.x + l.b * p.y + l.c) / sqrt(l.a * l.a + l.b * l.b)

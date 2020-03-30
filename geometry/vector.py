from math import sqrt

from geometry.point import Point
from constants import EPS


def cross_product(v1: Point, v2: Point) -> float:
    return v1.x * v2.y - v1.y * v2.x


def dot_product(v1: Point, v2: Point) -> float:
    return v1.x * v2.x + v1.y * v2.y


def sign(x: float) -> int:
    if abs(x) < EPS:
        return 0
    if (x > 0):
        return 1
    return -1


def length(v: Point) -> float:
    return sqrt(v.x * v.x + v.y * v.y)


def normalized(v: Point) -> Point:
    l = length(v)
    return v / l

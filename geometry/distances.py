from math import sqrt

from geometry.point import Point
from geometry.line import Line, line_from_points
from geometry.segment import Segment
from geometry.rectangle import Rectangle
from geometry.vector import length, dot_product, sign, normalized


def dist(p1: Point, p2: Point) -> float:
    return length(p2 - p1)


def dist_point_line(p: Point, l: Line) -> float:
    return (l.a * p.x + l.b * p.y + l.c) / sqrt(l.a * l.a + l.b * l.b)


def vector_dist_point_seg(p: Point, seg: Segment) -> Point:
    if sign(dot_product(seg.p2 - seg.p1, p - seg.p1)) == 1 and sign(dot_product(seg.p1 - seg.p2, p - seg.p2)) == 1:
        l = line_from_points(seg.p1, seg.p2)
        return normalized(l.get_normal()) * dist_point_line(p, l)
    v1 = p - seg.p1
    v2 = p - seg.p2
    if length(v1) < length(v2):
        return v1
    else:
        return v2


def vector_dist_point_rect(p: Point, rect: Rectangle) -> Point:
    v = []
    edges = rect.get_edges()
    for i in range(4):
        v.append(vector_dist_point_seg(p, edges[i]))
    for i in range(1, 4):
        if length(v[0]) > length(v[i]):
            v[0], v[i] = v[i], v[0]
    return v[0]

"""
Файл, содержащий функции пересечения различных геометрических объектов.
"""

from math import sqrt

from geometry.point import Point
from geometry.line import Line, line_from_points, point_on_line
from geometry.vector import sign, cross_product, normalized
from geometry.segment import Segment, point_on_segment
from geometry.rectangle import Rectangle
from geometry.circle import Circle
from geometry.distances import dist_point_line


def intersect_lines(l1: Line, l2: Line) -> Point:
    """
    Пересечение прямых.

    :param l1: первая прямая
    :param l2: вторая прямая
    :return: точка пересечения, если она существует, None иначе
    """
    if sign(cross_product(l1.get_normal(), l2.get_normal())) == 0:
        return None
    x = (l1.b * l2.c - l2.b * l1.c) / (l1.a * l2.b - l2.a * l1.b)
    y = (l1.a * l2.c - l2.a * l1.c) / (l2.a * l1.b - l1.a * l2.b)
    return Point(x, y)


def intersect_segments(seg1: Segment, seg2: Segment) -> Point:
    """
    Пересечение отрезков.

    :param seg1: первый отрезок
    :param seg2: второй отрезок
    :return: точка пересечения, если она существует, None иначе
    """
    if sign(cross_product(seg1.p2 - seg1.p1, seg2.p2 - seg2.p1)) == 0:
        if (sign(cross_product(seg1.p2 - seg1.p1, seg2.p1 - seg1.p1))) != 0:
            return None
        if point_on_segment(seg1.p1, seg2):
            return seg1.p1
        if point_on_segment(seg1.p2, seg2):
            return seg1.p2
        if point_on_segment(seg2.p1, seg1):
            return seg2.p1
        if point_on_segment(seg2.p2, seg1):
            return seg2.p2
        return None
    l1 = line_from_points(seg1.p1, seg1.p2)
    l2 = line_from_points(seg2.p1, seg2.p2)
    p = intersect_lines(l1, l2)
    if not p:
        return None
    if point_on_segment(p, seg1) and point_on_segment(p, seg2):
        return p
    return None


def intersect_seg_rect(seg: Segment, rect: Rectangle) -> Point:
    """
    Пересечение отрезка и прямоугольника. Возвращает ближайшую к началу отрезка точку пересечения.

    :param seg: отрезок
    :param rect: прямоугольник
    :return: точка пересечения, если она существует, None иначе
    """
    edges = rect.get_edges()
    p = []
    for i in range(4):
        p.append(intersect_segments(seg, edges[i]))
    for i in range(1, 4):
        if (not p[0]) or (p[i] and point_on_segment(p[i], Segment(seg.p1, p[0]))):
            p[0], p[i] = p[i], p[0]
    return p[0]


def intersect_line_circle(l: Line, c: Circle) -> (Point, Point):
    """
    Пересечение прямой и окружности.

    :param l: прямая
    :param c: окружность
    :return: пара точек пересечения, если их две, пара из точки пересечения и None, если она одна, пара из None и None
        иначе
    """
    to_line_dist = dist_point_line(c.center, l)
    if sign(abs(to_line_dist) - c.r) == 1:
        return None, None
    to_line = normalized(l.get_normal()) * (-to_line_dist)
    if sign(abs(to_line_dist) - c.r) == 0:
        return c.center + to_line, None
    aside_dist = sqrt(c.r * c.r - to_line_dist * to_line_dist)
    aside = normalized(l.get_parallel()) * aside_dist
    return c.center + to_line + aside, c.center + to_line - aside


def intersect_seg_circle(seg: Segment, c: Circle) -> Point:
    """
    Пересечение отрезка и окружности. Возвращает ближайшую к началу отрезка точку пересечения.

    :param seg: отрезок
    :param c: окружность
    :return: точка пересечения, если она существует, None иначе
    """
    l = line_from_points(seg.p1, seg.p2)
    p = list(intersect_line_circle(l, c))
    for i in range(2):
        if p[i] and not point_on_segment(p[i], seg):
            p[i] = None
    if not p[0]:
        p[0], p[1] = p[1], p[0]
    if not p[1]:
        return p[0]
    if point_on_segment(p[0], Segment(seg.p1, p[1])):
        return p[0]
    else:
        return p[1]


def intersect_circle_rect(c: Circle, rect: Rectangle) -> Point:
    """
    Пересечение окружности и прямоугольника. Возвращает некоторую любую тчку пересечения.

    :param c: окружность
    :param rect: прямоугольник
    :return: точка пересечения, если она существует, None иначе
    """
    edges = rect.get_edges()
    for i in range(4):
        p = intersect_seg_circle(edges[i], c)
        if p:
            return p
    return None

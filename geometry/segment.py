from geometry.point import Point
from geometry.vector import cross_product, dot_product, sign
from geometry.line import Line, line_from_points, intersect_lines
from geometry.rectangle import Rectangle
from constants import EPS


class Segment:
    def __init__(self, p1: Point = Point(), p2: Point = Point()):
        self.p1 = Point(p1.x, p1.y)
        self.p2 = Point(p2.x, p2.y)


def point_on_segment(p: Point, seg: Segment) -> bool:
    if sign(cross_product(p - seg.p1, seg.p2 - seg.p1)) != 0:
        return False
    return sign(dot_product(p - seg.p1, seg.p2 - seg.p1)) >= 0 and sign(dot_product(p - seg.p2, seg.p1 - seg.p2)) >= 0


def intersect_segments(seg1: Segment, seg2: Segment) -> Point:
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
    r1 = rect.top_left
    r2 = rect.bottom_right
    p = [Point() for _ in range(4)]
    p[0] = intersect_segments(seg, Segment(r1, Point(r1.x, r2.y)))
    p[1] = intersect_segments(seg, Segment(r2, Point(r1.x, r2.y)))
    p[2] = intersect_segments(seg, Segment(r1, Point(r2.x, r1.y)))
    p[3] = intersect_segments(seg, Segment(r2, Point(r2.x, r1.y)))
    for i in range(1, 4):
        if (not p[0]) or (p[i] and point_on_segment(p[i], Segment(seg.p1, p[0]))):
            p[0], p[i] = p[i], p[0]
    return p[0]

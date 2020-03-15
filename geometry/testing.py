from geometry.point import Point
from geometry.segment import Segment, point_on_segment, intersect_segments, intersect_seg_rect
from geometry.line import Line, line_from_points, intersect_lines
from geometry.rectangle import Rectangle


def main():
    x1, y1, x2, y2 = map(float, input().split())
    seg = Segment(Point(x1, y1), Point(x2, y2))
    rect = Rectangle(0, 0, 2, 2)
    p = intersect_seg_rect(seg, rect)
    if p:
        print(p.x, p.y)
    else:
        print("None")


if __name__ == '__main__':
    main()
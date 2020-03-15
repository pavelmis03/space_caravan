from geometry.point import Point
from geometry.segment import Segment
from geometry.rectangle import Rectangle
from geometry.circle import Circle
from geometry.intersections import intersect_seg_circle, intersert_circle_rect


def main():
    x1, y1, r = map(float, input().split())
    c = Circle(Point(x1, y1), r)
    rect = Rectangle(0, 0, 2, 2)
    q = intersert_circle_rect(c, rect)
    print(q)


if __name__ == '__main__':
    main()
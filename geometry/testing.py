from geometry.point import Point
from geometry.segment import Segment
from geometry.rectangle import Rectangle
from geometry.circle import Circle
from geometry.distances import vector_dist_point_rect


def main():
    rect = Rectangle(0, 0, 2, 2)
    while True:
        x1, y1 = map(float, input().split())
        v = vector_dist_point_rect(Point(x1, y1), rect)
        print(v.x, v.y)


if __name__ == '__main__':
    main()
"""
Файл, который можно использовать для тестирования геометрических средств (для этого нужно создать отдельную
конфигурацию запуска).
"""

from geometry.point import Point
from geometry.segment import Segment
from geometry.rectangle import Rectangle
from geometry.circle import Circle
from geometry.distances import vector_dist_point_rect
from geometry.intersections import intersect_seg_circle


def main():
    circle = Circle(Point(0, 0), 1)
    while True:
        x1, y1, x2, y2 = map(float, input().split())
        p = intersect_seg_circle(Segment(Point(x1, y1), Point(x2, y2)), circle)
        if p:
            print(p.x, p.y)
        else:
            print('None')


if __name__ == '__main__':
    main()
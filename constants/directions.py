from geometry.point import Point

DIRECTIONS = [
    Point(1, 0),
    Point(0, -1),
    Point(-1, 0),
    Point(0, 1),
]
side_di = [-1, 0, 1, 0]
side_dj = [0, 1, 0, -1]
diagonal_di = [-1, 1, 1, -1]
diagonal_dj = [1, 1, -1, -1]
rect_di = side_di + diagonal_di
rect_dj = side_dj + diagonal_dj
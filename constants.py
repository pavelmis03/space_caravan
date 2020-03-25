from geometry.point import Point


class Color:
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    ORANGE = (255, 180, 0)


DIRECTIONS = [
    Point(1, 0),
    Point(0, -1),
    Point(-1, 0),
    Point(0, 1),
]

di = [1, 0, -1, 0]
dj = [0, 1, 0, -1]



EPS = 1e-5

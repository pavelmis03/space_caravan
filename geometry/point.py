class Point:
    """
    Геометрическая точка, она же вектор. Я всегда против такого, но тут слабая типизация.

    :param x: абсцисса
    :param y: ордината
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)


def point_to_tuple(point):
    return point.x, point.y


def tuple_to_point(tuple):
    return Point(tuple[0], tuple[1])

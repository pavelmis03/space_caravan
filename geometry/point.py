from math import sqrt
from constants.math import EPS


class Point:
    """
    Геометрическая точка, она же вектор. Я всегда против такого, но тут слабая типизация.

    Поддерживает сложение, вычитание, а также умножение и деление на число.

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

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __eq__(self, other):
        dt = self - other
        distance = sqrt(dt.x * dt.x + dt.y * dt.y)
        return distance < EPS


def point_to_tuple(point):
    """
    Приводит точку к формату кортежа.

    :param point: точка
    :return: кортеж из координат точки
    """
    return point.x, point.y


def tuple_to_point(tuple):
    """
    Приводит кортеж к формату точки.

    :param tuple: кортеж
    :return: точка с координатами из кортежа
    """
    return Point(tuple[0], tuple[1])

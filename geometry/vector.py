"""
В геометрических средствах проекта для представления вектора используется класс точки Point. В этом файле находятся
функции, работающие с точками как с векторами.
"""

from math import sqrt

from geometry.point import Point
from constants import EPS


def cross_product(v1: Point, v2: Point) -> float:
    """
    Псевдоскалярное, или косое, произведение векторов.

    :param v1: первый вектор
    :param v2: второй вектор
    :return: числовое значение
    """
    return v1.x * v2.y - v1.y * v2.x


def dot_product(v1: Point, v2: Point) -> float:
    """
    Скалярное произведение векторов.

    :param v1: первый вектор
    :param v2: второй вектор
    :return: числовое значение
    """
    return v1.x * v2.x + v1.y * v2.y


def sign(x: float) -> int:
    """
    Знак числа. Эта процедура нужна для геометрии на основе нецелых чисел: для значений по модулю меньших EPS она
    возвращает 0.

    :param x: число
    :return: знак числа (0, если число не отличимо от нуля; 1, если больше; -1, если меньше)
    """
    if abs(x) < EPS:
        return 0
    if (x > 0):
        return 1
    return -1


def length(v: Point) -> float:
    """
    Длина вектора.

    :param v: вектор
    :return: числовое значение
    """
    return sqrt(v.x * v.x + v.y * v.y)


def normalized(v: Point) -> Point:
    """
    Вектор единичной длины, сонаправленный с данным.

    :param v: вектор
    :return: соответствующий вектор единичной длины
    """
    l = length(v)
    return v / l

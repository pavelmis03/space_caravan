"""
В геометрических средствах проекта для представления вектора используется класс точки Point. В этом файле находятся
функции, работающие с точками как с векторами.
"""

from math import sqrt, sin, cos, atan2
from typing import List

from geometry.point import Point
from constants.math import EPS


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


def length_squared(v: Point) -> float:
    """
    Квадрат длины вектора.

    :param v: вектор
    :return: числовое значение
    """
    return v.x * v.x + v.y * v.y


def length(v: Point) -> float:
    """
    Длина вектора.

    :param v: вектор
    :return: числовое значение
    """
    return sqrt(length_squared(v))


def polar_angle(v: Point) -> float:
    """
    Полярный угол вектора. Координаты кривые, поэтому y с минусом.

    :param v: вектор
    :return: числовое значение
    """
    return atan2(-v.y, v.x)


def normalized(v: Point) -> Point:
    """
    Вектор единичной длины, сонаправленный с данным.

    :param v: вектор
    :return: соответствующий вектор единичной длины
    """
    l = length(v)
    return v / l


def vector_from_length_angle(l: float, angle: float) -> Point:
    """
    Построение вектора по длине и полярному углу. Координаты кривые, поэтому y с минусом.

    :param l: длина
    :param angle: полярный угол
    :return: соответствующий вектор
    """
    return Point(l * cos(angle), -l * sin(angle))


def get_min_vector(vectors: List[Point]) -> Point:
    """
    Получить минимальный по длине вектор из данного набора.
    """
    result = vectors[0]
    for i in range(1, len(vectors)):
        if length(vectors[i]) < length(result):
            result = vectors[i]
    return result

"""
вспомогательный модуль для простых математических функций
"""
from constants.math import EPS


def sign(x: int) -> int:
    """
    Получить знак целого числа.

    :param x: число
    :return: 1, -1 или 0
    """
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def is_floats_equal(first: float, second: float) -> bool:
    """
    вещественные числа нельзя сравнивать через == из-за особенностей
    их хранения в памяти
    """
    return abs(first - second) < EPS


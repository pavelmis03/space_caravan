from geometry.optimized.segment import get_vector
from geometry.point import Point
from geometry.vector import cross_product, sign


def is_point_in_triangle(p: Point, p1: Point, p2: Point, p3: Point) -> bool:
    """
    Находится ли точка в треугольнике. Проверка через косые произведения

    :param p: Исходная точка
    :param p1: Первая точка треугольника
    :param p2: Вторая точка
    :param p3: Третья
    :return: True, если находится. Иначе False
    """
    mult1 = cross_product(get_vector(p, p1), get_vector(p1, p2))
    mult2 = cross_product(get_vector(p, p2), get_vector(p2, p3))
    if sign(mult1) != sign(mult2):
        return False
    mult3 = cross_product(get_vector(p, p3), get_vector(p3, p1))
    return sign(mult1) == sign(mult3)
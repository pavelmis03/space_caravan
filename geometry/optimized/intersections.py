from geometry.optimized.segment import StaticSegment, get_vector
from geometry.vector import cross_product
from geometry.optimized.rectangle import StaticRectangle


def is_segments_intersect(a: StaticSegment, b: StaticSegment) -> bool:
    """
    Пересечение статических отрезков.

    :param a: статический отрезок
    :param b: статический отрезок
    :return: bool
    """
    """
    Ограничивающие прямоугольники
    """
    if a.max_x < b.min_x or b.max_x < a.min_x or \
            a.max_y < b.min_y or b.max_y < a.min_y:
        return False

    """
    Проверка через косые произведения. Работает быстрее поиска пересечения прямых.
    """
    return (cross_product(a.vector, get_vector(a.p1, b.p1)) *
            cross_product(a.vector, get_vector(a.p1, b.p2)) <= 0.0) and \
        (cross_product(b.vector, get_vector(b.p1, a.p1)) *
         cross_product(b.vector, get_vector(b.p1, a.p2)) <= 0.0)


def is_seg_rect_intersect(seg: StaticSegment, rect: StaticRectangle) -> bool:
    """
    пересекаются ли статические отрезок и прямоугольник
    """
    edges = rect.get_edges()
    for i in range(len(edges)):
        if is_segments_intersect(seg, edges[i]):
            return True

    return False

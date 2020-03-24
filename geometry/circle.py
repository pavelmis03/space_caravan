from geometry.point import Point


class Circle:
    """
    Класс геометрической окружности.

    :param center: центр
    :param r: радиус
    """
    def __init__(self, center: Point = Point(), r: float = 0):
        self.center = center
        self.r = r

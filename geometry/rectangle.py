from pygame import Rect
from typing import List

from geometry.point import Point, point_to_tuple
from geometry.segment import Segment


class Rectangle:
    """
    Прямоугольник. Почти pygame.Rect, только работает с точками Point.

    :param left_x: абсцисса левой границы (меньшая)
    :param up_y: ордината верхней границы (меньшая)
    :param right_x: абсцисса правой границы (большая)
    :param down_y: ордината нижней границы (большая)
    """
    def __init__(self, left_x: float=0, up_y: float=0, right_x: float=0, down_y: float=0):
        self._top_left = Point(left_x, up_y)
        self._bottom_right = Point(right_x, down_y)
        self._center = (self._top_left + self._bottom_right) * 0.5
        self._width = right_x - left_x
        self._height = down_y - up_y

    def move(self, movement):
        """
        Передвигает прямоугольник параллельным переносом на заданный вектор.

        :param movement: вектор переноса
        """
        self._top_left += movement
        self._bottom_right += movement
        self._center += movement

    @property
    def center(self):
        """
        Центр прямоугольника.
        """
        return self._center

    @center.setter
    def center(self, new_center):
        movement = new_center - self._center
        self.move(movement)

    @property
    def top_left(self):
        """
        Верхний левый угол прямоугольника.
        """
        return self._top_left

    @property
    def left(self) -> float:
        return self._top_left.x

    @property
    def right(self) -> float:
        return self._bottom_right.x

    @property
    def top(self) -> float:
        return self._top_left.y

    @property
    def bottom(self) -> float:
        return self._bottom_right.y

    @top_left.setter
    def top_left(self, new_top_left):
        movement = new_top_left - self._top_left
        self.move(movement)

    @property
    def bottom_right(self):
        """
        Правый нижний угол прямоугольника.
        """
        return self._bottom_right

    @bottom_right.setter
    def bottom_right(self, new_bottom_right):
        movement = new_bottom_right - self._bottom_right
        self.move(movement)

    @property
    def width(self):
        """
        Ширина прямоугольника.
        """
        return self._width

    @width.setter
    def width(self, new_width):
        movement = Point((new_width - self._width) / 2, 0)
        self._width = new_width
        self._top_left -= movement
        self._bottom_right += movement

    @property
    def height(self):
        """
        Высота прямоугольника.
        """
        return self._height

    @height.setter
    def height(self, new_height):
        movement = Point(0, (new_height - self._height) / 2)
        self._height = new_height
        self._top_left -= movement
        self._bottom_right += movement

    def in_inside(self, point):
        """
        Проверка принадлежности точки прямоугольнику.

        :param point: точка
        :return: логическое значение
        """
        if self._top_left.x > point.x or self._top_left.y > point.y:
            return False
        if self._bottom_right.x < point.x or self._bottom_right.y < point.y:
            return False
        return True

    def is_empty(self) -> bool:
        """
        Вырожден ли прямоугольник (отрицательна ли ширина или высота).

        :return: логическое значение
        """
        return self._width < 0 or self._height < 0

    def get_vertexes(self) -> List[Point]:
        """
        Вершины прямоугольника.

        :return: список точек - вершин прямоугольника
        Порядок вершин: левая верхняя, правая верхняя,
                        правая нижняя, левая нижняя
        """
        r1 = self._top_left
        r2 = self._bottom_right
        p = [r1, Point(r2.x, r1.y), r2, Point(r1.x, r2.y)]
        return p

    def get_edges(self) -> List[Segment]:
        """
        Стороны прямоугольника.

        :return: список отрезков - сторон прямоугольника
        Порядок сторон(отрезков): верхняя, правая, нижняя, левая)
        """
        p = self.get_vertexes()
        edges = []
        for i in range(4):
            edges.append(Segment(p[i], p[(i + 1) % 4]))
        return edges


def rect_to_rectangle(rect):
    """
    Приводит pygame.Rect к формату прямоугольника Rectangle.

    :param rect: объект pygame.Rect
    :return: соответствующий Rectangle
    """
    rectangle = Rectangle(rect.left, rect.top, rect.right, rect.bottom)
    return rectangle


def rectangle_to_rect(rectangle):
    """
    Приводит прямоугольник Rectangle к формату pygame.Rect.

    :param rectangle: объект Rectangle
    :return: соответствующий pygame.Rect
    """
    return Rect(point_to_tuple(rectangle.top_left), (rectangle.width, rectangle.height))


def create_rectangle_with_center(center: Point, w: float, h: float) -> Rectangle:
    """
    Создает прямоугольник с заданным центром.

    :param center: точка центра
    :param w: ширина
    :param h: высота
    :return: соответствующий прямоугольник
    """
    return Rectangle(center.x - w / 2, center.y - h / 2, center.x + w / 2, center.y + h / 2)

def create_rectangle_with_left_top(left_top: Point, w: float, h: float) -> Rectangle:
    """
    Создает прямоугольник с заданным левым верхним углом.

    :param left_top: точка верхнего левого угла
    :param w: ширина
    :param h: высота
    :return: соответствующий прямоугольник
    """
    return Rectangle(left_top.x, left_top.y, left_top.x + w, left_top.y + h)

def tuple_to_rectangle(tuple):
    """
    Приводит кортеж из координат левого верхнего и правого нижнего углов прямоугольника соответственно к формату
    прямоугольника Rectangle.

    :param tuple: кортеж с координатами
    :return: соответствующий Rectangle
    """
    return Rectangle(tuple[0], tuple[1], tuple[2], tuple[3])


def get_rectangle_copy(rectangle: Rectangle) -> Rectangle:
    return Rectangle(rectangle.top_left.x, rectangle.top_left.y,
                     rectangle.bottom_right.x, rectangle.bottom_right.y)


def intersect(rectangle1, rectangle2):
    """
    Пересечение прямоугольников.

    :param rectangle1: первый прямоугольник
    :param rectangle2: второй прямоугольник
    :return: прямоугольник - пересечение первых двух
    """
    left_x = max(rectangle1.top_left.x, rectangle2.top_left.x)
    right_x = min(rectangle1.bottom_right.x, rectangle2.bottom_right.x)
    top_y = max(rectangle1.top_left.y, rectangle2.top_left.y)
    bottom_y = min(rectangle1.bottom_right.y, rectangle2.bottom_right.y)
    return Rectangle(left_x, top_y, right_x, bottom_y)

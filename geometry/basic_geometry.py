from pygame import Rect


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


class Rectangle:
    """
    Прямоугольник

    :param left_x: абсцисса левой границы (меньшая)
    :param up_y: ордината верхней границы (меньшая)
    :param right_x: абсцисса правой границы (большая)
    :param down_y: ордината нижней границы (большая)
    """
    def __init__(self, left_x=0, up_y=0, right_x=0, down_y=0):
        self._top_left = Point(left_x, up_y)
        self._bottom_right = Point(right_x, down_y)
        self._center = (self._top_left + self._bottom_right) * 0.5
        self._width = right_x - left_x
        self._height = down_y - up_y

    def move(self, movement):
        self._top_left += movement
        self.bottom_right += movement
        self.center += movement

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, new_center):
        movement = new_center - self._center
        self.move(movement)

    @property
    def top_left(self):
        return self._top_left

    @top_left.setter
    def top_left(self, new_top_left):
        movement = new_top_left - self._top_left
        self.move(movement)

    @property
    def bottom_right(self):
        return self._bottom_right

    @bottom_right.setter
    def bottom_right(self, new_bottom_right):
        movement = new_bottom_right - self._bottom_right
        self.move(movement)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new_width):
        movement = Point((new_width - self._width) / 2, 0)
        self._width = new_width
        self._top_left -= movement
        self._bottom_right += movement

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height):
        movement = Point(0, (new_height - self._height) / 2)
        self._height = new_height
        self._top_left -= movement
        self._bottom_right += movement


def rectangle_from_rect(rect):
    rectangle = Rectangle(rect.left, rect.top, rect.right, rect.bottom)
    return rectangle


def rect_from_rectangle(rectangle):
    rect = Rect()
    rect.left = rectangle.top_left.x
    rect.top = rectangle.top_left.y
    rect.right = rectangle.bottom_right.x
    rect.bottom = rectangle.bottom_right.y
    return rect

from typing import List, Tuple

from random import randint
from utils.random import is_random_proc

class GridRectangle:
    def __init__(self, left_top_index: Tuple[int, int],
                 bottom_right_index: Tuple[int, int]):
        self._left_top_index = left_top_index
        self._bottom_right_index = bottom_right_index

    def is_index_in_inside(self, i: int, j: int) -> bool:
        return self._left_top_index[0] <= i <= self._bottom_right_index[0] and \
               self._left_top_index[1] <= j <= self._bottom_right_index[1]

    @property
    def top_index(self):
        return self._left_top_index[0]

    @property
    def left_index(self):
        return self._left_top_index[1]

    @property
    def bottom_index(self):
        return self._bottom_right_index[0]

    @property
    def right_index(self):
        return self._bottom_right_index[1]

class RectSplitter:
    """
    рекурсивный алгоритм разбиения:
    выбирается направление, по которому будет
    разделяться прямоугольник (вертикальное, горизонтальное).
    Далее выбирается положение прямой (положение по горизонтали
    и по вертикали соответственно). После этого прямоугольник делится
    на 2 прямоугольника этой прямой. Вызывается рекурсивная функция от них (split_rectangle).

    Условие выхода из рекурсии - невозможность такого разбиения (хотя бы по одному из направлений),
    при котором для каждого прямоугольника выполняется:
    -ширина >= min_w
    -высота >= min_h
    или
    площадь текущего прямоугольника < min_area
    """
    def __init__(self, arr: List[List[int]], min_area: int, min_w: int, min_h: int):
        self.arr = arr
        self.min_area = min_area
        self.min_size = [min_h, min_w]
        self.last_rect_num = 0

        self.rectangles = []

    def start_random_split(self):
        self.split_rectangle([0, 0], [len(self.arr) - 1, len(self.arr[0]) - 1])

    def split_rectangle(self, pos0: List[int], pos1: List[int]):
        """
        pos_0 - позиция левой верхней клетки прямоугольника
        pos_1 - позиция правой нижней клетки прямоугольника

        :param pos0_y:
        :param pos0_x:
        :param pos1_y:
        :param pos1_x:
        :return:
        """
        w = pos1[1] - pos0[1] + 1
        h = pos1[0] - pos0[0] + 1
        if w * h < self.min_area:
            self.fill_rect(pos0, pos1)
            return

        wall_size = 1

        min_pos = []
        for i in range(len(pos0)):
            min_pos.append(pos0[i] + self.min_size[i] + wall_size)

        max_pos = []
        for i in range(len(pos1)):
            max_pos.append(pos1[i] - self.min_size[i] - wall_size)

        self.choose_direction_and_split(pos0, pos1, min_pos, max_pos)

    def choose_direction_and_split(self, pos0: List[int], pos1: List[int],
                                   min_pos: List[int], max_pos: List[int]):
        """
        если нельзя разбить, тогда вызывается fill_rect,
        если можно только по одному из направлений, разбивается по нему,
        иначе выбирается рандомное направление.
        """
        split_directions = 2
        for i in range(len(min_pos)):
            if min_pos[i] > max_pos[i]:
                split_directions -= 1

        if not split_directions:
            self.fill_rect(pos0, pos1)
            return

        if split_directions == 1:
            if min_pos[0] <= max_pos[0]:
                self.split_horizontally(pos0, pos1, randint(min_pos[0], max_pos[0]))
            else:
                self.split_vertical(pos0, pos1, randint(min_pos[1], max_pos[1]))
            return

        if is_random_proc():
            self.split_horizontally(pos0, pos1, randint(min_pos[0], max_pos[0]))
        else:
            self.split_vertical(pos0, pos1, randint(min_pos[1], max_pos[1]))

    def split_horizontally(self, pos0, pos1, new_pos):
        self.split_rectangle(pos0, [new_pos, pos1[1]])
        self.split_rectangle([new_pos, pos0[1]], pos1)

    def split_vertical(self, pos0, pos1, new_pos):
        self.split_rectangle(pos0, [pos1[0], new_pos])
        self.split_rectangle([pos0[0], new_pos], pos1)

    @property
    def rects_count(self):
        return self.last_rect_num + 1

    def fill_rect(self, pos0: List[int], pos1: List[int]):
        new_rectangle = GridRectangle((pos0[0], pos0[1]),
                                      (pos1[0], pos1[1]))
        self.rectangles.append(new_rectangle)
        self.last_rect_num += 1

        for i in range(pos0[0] + 1, pos1[0]):
            for j in range(pos0[1] + 1, pos1[1]):
                self.arr[i][j] = self.last_rect_num
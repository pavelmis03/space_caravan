from typing import List

from random import randint
from utils.random import is_random_proc

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
        self.is_vertex_of_rect = [[False] * len(self.arr[0]) for i in range(len(self.arr))]
        self.last_rect_num = 0

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
            min_pos.append(pos0[i] + self.min_size[i] + 2 * wall_size)

        max_pos = []
        for i in range(len(pos1)):
            max_pos.append(pos1[i] - self.min_size[i] - 2 * wall_size)

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
        self.split_rectangle([new_pos + 1, pos0[1]], pos1)

    def split_vertical(self, pos0, pos1, new_pos):
        self.split_rectangle(pos0, [pos1[0], new_pos])
        self.split_rectangle([pos0[0], new_pos + 1], pos1)

    @property
    def rects_count(self):
        return self.last_rect_num + 1

    def fill_rect(self, pos0: List[int], pos1: List[int]):
        self.last_rect_num += 1

        self.is_vertex_of_rect[pos0[0]][pos0[1]] = True
        self.is_vertex_of_rect[pos0[0]][pos1[1]] = True
        self.is_vertex_of_rect[pos1[0]][pos0[1]] = True
        self.is_vertex_of_rect[pos1[0]][pos1[1]] = True

        for i in range(pos0[0], pos1[0] + 1):
            self.arr[i][pos0[1]] = self.arr[i][pos1[1]] = self.last_rect_num

        for i in range(pos0[1], pos1[1] + 1):
            self.arr[pos0[0]][i] = self.arr[pos1[0]][i] = self.last_rect_num
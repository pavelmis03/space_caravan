from typing import List, Tuple, Dict

from random import randint
from utils.random import is_random_proc


class GridRectangle:
    """
    Прямоугольник сетки, состоящий из индексов
    """

    def __init__(self, left_top_index: Tuple[int, int],
                 bottom_right_index: Tuple[int, int]):
        self.left_top_index = left_top_index
        self.bottom_right_index = bottom_right_index

    def is_index_inside(self, i: int, j: int) -> bool:
        """
        Внутри ли индекс прямоугольника
        """
        return self.left_top_index[0] <= i <= self.bottom_right_index[0] and \
            self.left_top_index[1] <= j <= self.bottom_right_index[1]

    @property
    def top_index(self):
        """
        минимальный i
        """
        return self.left_top_index[0]

    @property
    def left_index(self):
        """
        минимальный j
        """
        return self.left_top_index[1]

    @property
    def bottom_index(self):
        """
        максимальный i
        """
        return self.bottom_right_index[0]

    @property
    def right_index(self):
        """
        максимальный j
        """
        return self.bottom_right_index[1]

    def to_dict(self) -> Dict:
        return {
            'left_top_index': [self.left_top_index[0], self.left_top_index[1]],
            'bottom_right_index': [self.bottom_right_index[0], self.bottom_right_index[1]],
            'classname': self.__class__.__name__
        }

    def from_dict(self, dict: Dict):
        self.left_top_index = (
            dict['left_top_index'][0], dict['left_top_index'][1])
        self.bottom_right_index = (
            dict['bottom_right_index'][0], dict['bottom_right_index'][1])


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
        self.__min_area = min_area
        self.__min_size = [min_h, min_w]

        self.rectangles = []

    def start_random_split(self):
        """
        Начать разбиение всего self.arr
        """
        self.__split_rectangle(
            [0, 0], [len(self.arr) - 1, len(self.arr[0]) - 1])

    def __split_rectangle(self, pos0: List[int], pos1: List[int]):
        """
        Начать разбиение прямоугольника.

        pos_0 - позиция левой верхней клетки прямоугольника
        pos_1 - позиция правой нижней клетки прямоугольника
        :return:
        """
        w = pos1[1] - pos0[1] + 1
        h = pos1[0] - pos0[0] + 1
        if w * h < self.__min_area:
            self.__fill_rect(pos0, pos1)
            return

        wall_size = 1

        min_pos = []
        for i in range(len(pos0)):
            min_pos.append(pos0[i] + self.__min_size[i] + wall_size)

        max_pos = []
        for i in range(len(pos1)):
            max_pos.append(pos1[i] - self.__min_size[i] - wall_size)

        self.__choose_direction_and_split(pos0, pos1, min_pos, max_pos)

    def __choose_direction_and_split(self, pos0: List[int], pos1: List[int],
                                     min_pos: List[int], max_pos: List[int]):
        """

        :param pos0: левый верхний индекс прямоугольника, в котором происходит split
        :param pos1: правый нижний индекс прямоугольника, в котором происходит split
        :param min_pos: минимальные индексы, по которым может происходить разбиение
        :param max_pos: максимальные индексы, по которым может происходить разбиение
        :return:
        """
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
            self.__fill_rect(pos0, pos1)
            return

        if split_directions == 1:
            if min_pos[0] <= max_pos[0]:
                self.__split_horizontally(
                    pos0, pos1, randint(min_pos[0], max_pos[0]))
            else:
                self.__split_vertical(
                    pos0, pos1, randint(min_pos[1], max_pos[1]))
            return

        if is_random_proc():
            self.__split_horizontally(
                pos0, pos1, randint(min_pos[0], max_pos[0]))
        else:
            self.__split_vertical(pos0, pos1, randint(min_pos[1], max_pos[1]))

    def __split_horizontally(self, pos0: List[int], pos1: List[int], new_pos: List[int]):
        """
        Разбить прямоугольник горизонтальной чертой
        :param pos0: левый верхний индекс прямоугольника, в котором происходит split
        :param pos1: правый нижний индекс прямоугольника, в котором происходит split
        :param new_pos: индекс, по которому идет разбиение
        """
        self.__split_rectangle(pos0, [new_pos, pos1[1]])
        self.__split_rectangle([new_pos, pos0[1]], pos1)

    def __split_vertical(self, pos0: List[int], pos1: List[int], new_pos: int):
        """
        Разбить прямоугольник вертикальной чертой
        :param pos0: левый верхний индекс прямоугольника, в котором происходит split
        :param pos1: правый нижний индекс прямоугольника, в котором происходит split
        :param new_pos: индекс, по которому идет разбиение
        """
        self.__split_rectangle(pos0, [pos1[0], new_pos])
        self.__split_rectangle([pos0[0], new_pos], pos1)

    @property
    def rects_colors_count(self) -> int:
        """
        Количество цветов. Добавляется единица, чтобы цвет 0 (цвет стены) учитывался.
        """
        return len(self.rectangles) + 1

    def __fill_rect(self, pos0: List[int], pos1: List[int]):
        """
        Заполнить прямоугольник его цветом.
        :param pos0: левый верхний угол
        :param pos1: правый нижний угол
        """
        new_rectangle = GridRectangle((pos0[0], pos0[1]),
                                      (pos1[0], pos1[1]))
        self.rectangles.append(new_rectangle)

        for i in range(pos0[0] + 1, pos1[0]):
            for j in range(pos0[1] + 1, pos1[1]):
                self.arr[i][j] = len(self.rectangles)

    def get_arr_after_split(self) -> List[List[int]]:
        """
        получить список после разбиения.
        """
        result = []
        for i in range(len(self.arr)):
            result.append([])
            for j in range(len(self.arr[i])):
                result[i].append(self.arr[i][j])
        return result

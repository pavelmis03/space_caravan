from typing import List

from geometry.point import Point

from random import randint, shuffle
from utils.random import is_random_proc

from utils.disjoint_set import DisjointSet

from drawable_objects.player import GameSprite

from controller.controller import Controller
from scenes.base import Scene

class Grid:
    def __init__(self, screen: Scene, controller: Controller,
                 width: int=100, height: int=100, default_value=0):
        '''
        :param width:
        :param height:
        :param default_value:
        '''
        self.screen = screen
        self.controller = controller

        self.width = width
        self.height = height
        self.arr = [[default_value] * self.width for i in range(self.height)]

    def print_arr(self):
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                print(self.arr[i][j], end='')
            print()


class GeneratedGird(Grid):
    '''
    Сетка для данжа.
    Результат генерации - заполнение исходного прямоугольника фигурами
    с углами 270 и 90 градусов.
    '''
    def __init__(self, screen: Scene, controller: Controller,
                 cell_width: int, cell_height: int,
                 width: int=100, height: int=100,
                 min_area: int=16, min_w: int=10, min_h: int=10):
        '''
        :param width:
        :param height:
        :param default_value:
        '''
        super().__init__(screen, controller, width, height, 0)

        self.cell_width = cell_width
        self.cell_height = cell_height

        self.rect_splitter = RectSplitter(self.arr, min_area, min_w, min_h)
        self.generate()
        self.transform_ints_to_objects()

    def process_draw(self, p: Point):
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                self.arr[i][j].process_draw(p)

    def process_logic(self):
        pass

    def transform_ints_to_objects(self):
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                pos_x = j * self.cell_width
                pos_y = i * self.cell_height
                if self.arr[i][j]:
                    self.arr[i][j] = GameSprite(self.screen, self.controller,
                                                'images/floor.png', Point(pos_x, pos_y))
                else:
                    self.arr[i][j] = GameSprite(self.screen, self.controller,
                                                'images/wall.png', Point(pos_x, pos_y))

    def generate(self):
        '''
        рекурсивный алгоритм генерации:
        выбирается направление, по которому будет
        разделяться прямоугольник (вертикальное, горизонтальное).
        Далее выбирается положение прямой (положение по горизонтали
        и по вертикали соответственно). После этого прямоугольник делится
        на 2 прямоугольника этой прямой. Вызывается рекурсивная функция от них.

        Условие выхода из рекурсии - невозможность такого разбиения (хотя бы по одному из направлений),
        при котором для каждого прямоугольника выполняется:
        -ширина >= min_w
        -высота >= min_h
        или
        площадь текущего прямоугольника < min_area

        После проводятся ребра (двери) между полученными фигурами или объединение фигур.
        Граф связный, но не обязательно является деревом.
        '''
        self.rect_splitter.start_random_split()
        self.edges = []
        '''
        edge - list([i1, j1, color1], [i2, j2, color2]) 
        '''
        self.save_edges_between_rects(self.edges)
        shuffle(self.edges)
        self.connect_rects()
        self.print_arr()

    def save_edges_between_rects(self, res):
        '''
        Чтобы не дублировать ребра, сохраняются только
        ребра из клетки влево и из клетки вверх
        :param res:
        :return:
        '''
        dy = [-1, 0]
        dx = [0, -1]
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                for k in range(len(dy)):
                    new_i = i + dy[k]
                    new_j = j + dx[k]

                    if new_i < 0 or new_j < 0:
                        continue

                    if not (self.arr[i][j] and self.arr[new_i][new_j]):
                        continue # 0 - внутренняя часть rect

                    if self.rect_splitter.is_vertex_of_rect[i][j] or \
                        self.rect_splitter.is_vertex_of_rect[new_i][new_j]:
                        continue

                    if self.arr[i][j] == self.arr[new_i][new_j]:
                        continue
                    res.append([[i, j, self.arr[i][j]],
                                [new_i, new_j, self.arr[new_i][new_j]]])

    def connect_rects(self):
        self.dis_set = DisjointSet(self.rect_splitter.rects_count + 1)
        for i in range(len(self.edges)):
            edge = self.edges[i]
            first_color = edge[0][2]
            second_color = edge[1][2]
            if not self.dis_set.check(first_color, second_color):
                self.dis_set.union(first_color, second_color)
                self.arr[edge[0][0]][edge[0][1]] = \
                self.arr[edge[1][0]][edge[1][1]] = 0 # делаем пустой проход между ними


class RectSplitter:
    def __init__(self, arr: List[int], min_area: int, min_w: int, min_h: int):
        self.arr = arr
        self.min_area = min_area
        self.min_size = [min_h, min_w]
        self.rects_count = 0
        self.is_vertex_of_rect = [[False] * len(self.arr[0]) for i in range(len(self.arr))]

    def start_random_split(self):
        self.split_rectangle([0, 0], [len(self.arr) - 1, len(self.arr[0]) - 1])

    def split_rectangle(self, pos0: List[int], pos1: List[int]):
        '''
        pos_0 - позиция левой верхней клетки прямоугольника
        pos_1 - позиция правой нижней клетки прямоугольника

        :param pos0_y:
        :param pos0_x:
        :param pos1_y:
        :param pos1_x:
        :return:
        '''
        w = pos1[1] - pos0[0] + 1
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

        for i in range(len(min_pos)):
            if min_pos[i] > max_pos[i]:
                self.fill_rect(pos0, pos1)
                return

        '''
        либо вертикальная, либо горизонатальная прямая
        '''
        if is_random_proc():
            # горизонтальная
            new_pos = randint(min_pos[0], max_pos[0])
            self.split_rectangle(pos0, [new_pos, pos1[1]])
            self.split_rectangle([new_pos + 1, pos0[1]], pos1)
        else:
            new_pos = randint(min_pos[1], max_pos[1])
            self.split_rectangle(pos0, [pos1[0], new_pos])
            self.split_rectangle([pos0[0], new_pos + 1], pos1)

    def fill_rect(self, pos0: List[int], pos1: List[int]):
        self.rects_count += 1

        self.is_vertex_of_rect[pos0[0]][pos0[1]] = True
        self.is_vertex_of_rect[pos0[0]][pos1[1]] = True
        self.is_vertex_of_rect[pos1[0]][pos0[1]] = True
        self.is_vertex_of_rect[pos1[0]][pos1[1]] = True

        for i in range(pos0[0], pos1[0] + 1):
            self.arr[i][pos0[1]] = self.arr[i][pos1[1]] = self.rects_count

        for i in range(pos0[1], pos1[1] + 1):
            self.arr[pos0[0]][i] = self.arr[pos1[0]][i] = self.rects_count
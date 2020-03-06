from typing import List

from geometry.point import Point

from random import randint
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
                 width: int=200, height: int=200,
                 min_area: int=100, min_w: int=8, min_h: int=8):
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
        '''
        edge - list([i1, j1, color1], [i2, j2, color2]) 
        '''
        self.edges = []
        self.save_edges_between_rects(self.edges)
        self.shuffle(self.edges)

        self.union_rects()
        self.delete_edges_between_united_rects()

        self.edges = []
        self.save_edges_between_rects(self.edges)
        self.shuffle(self.edges)

        self.connect_rects()
        self.print_arr()

    def shuffle(self, arr):
        for i in range(len(arr) - 1, 0, -1):
            j = randint(0, i + 1)

            arr[i], arr[j] = arr[j], arr[i]

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

    def get_union_chance(self, rect_num1: int, rect_num2: int) -> int:
        if self.dis_set.check(rect_num1, rect_num2):
            return 0

        new_figure_count = self.figures_count[rect_num1] * \
                            self.figures_count[rect_num2]

        START_CHANCE = 20
        return START_CHANCE // (new_figure_count ** 2)

    def union_rects(self):
        """
        делает из прямоугольников фигуры с углами 270 и 90 градусов,
        объединяя некоторые прямоугольники

        :return:
        """
        self.figures_count = [1 for i in range(self.rect_splitter.rects_count + 1)]
        self.dis_set = DisjointSet(self.rect_splitter.rects_count + 1)

        for i in range(len(self.edges)):
            edge = self.edges[i]
            first_color = edge[0][2]
            second_color = edge[1][2]
            chance = self.get_union_chance(first_color, second_color)
            if is_random_proc(chance):
                self.dis_set.union(first_color, second_color)
                new_figure_count = self.figures_count[first_color] + \
                                    self.figures_count[second_color]

                self.figures_count[first_color] = new_figure_count
                self.figures_count[second_color] = new_figure_count

    def delete_edges_between_united_rects(self):
        dy = [-1, 0]
        dx = [0, -1]
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                if not self.arr[i]:
                    continue
                for k in range(len(dy)):
                    new_i = i + dy[k]
                    new_j = j + dx[k]

                    if new_i < 0 or new_j < 0:
                        continue

                    if not self.arr[new_i][new_j]:
                        continue

                    if self.arr[i][j] == self.arr[new_i][new_j]:
                        continue

                    if self.dis_set.check(self.arr[i][j], self.arr[new_i][new_j]):
                        if not self.rect_splitter.is_vertex_of_rect[i][j]:
                            self.arr[i][j] = 0
                        if not self.rect_splitter.is_vertex_of_rect[new_i][new_j]:
                            self.arr[new_i][new_j] = 0

        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                if self.arr[i][j]:
                    self.arr[i][j] = self.dis_set.get_parent(self.arr[i][j])

        #return
        dy = [-1, 0, 1, 0]
        dx = [0, 1, 0, -1]
        for i in range(1, len(self.arr) - 1):
            for j in range(1, len(self.arr[i]) - 1):
                if not self.rect_splitter.is_vertex_of_rect[i][j]:
                    continue
                has_side_cell = False
                for k in range(len(dy)):
                    new_i = i + dy[k]
                    new_j = j + dx[k]
                    if self.arr[new_i][new_j] and \
                        not self.rect_splitter.is_vertex_of_rect[new_i][new_j]:
                        has_side_cell = True
                        break

                if not has_side_cell:
                    self.arr[i][j] = 0


    def connect_rects(self):
        """
        делает проходы(двери) между прямоугольниками.

        :return:
        """
        self.dis_set = DisjointSet(self.rect_splitter.rects_count + 1)
        for i in range(len(self.edges)):
            edge = self.edges[i]
            first_color = edge[0][2]
            second_color = edge[1][2]
            if not self.dis_set.check(first_color, second_color):
                self.dis_set.union(first_color, second_color)
                self.arr[edge[0][0]][edge[0][1]] = 0
                self.arr[edge[1][0]][edge[1][1]] = 0 # делаем пустой проход между ними
                continue

            CHANCE_EXTRA_CONNECTION = 1
            if is_random_proc(CHANCE_EXTRA_CONNECTION):
                self.arr[edge[0][0]][edge[0][1]] = 0
                self.arr[edge[1][0]][edge[1][1]] = 0  # делаем пустой проход между ними


class RectSplitter:
    def __init__(self, arr: List[int], min_area: int, min_w: int, min_h: int):
        self.arr = arr
        self.min_area = min_area
        self.min_size = [min_h, min_w]
        self.rects_count = 0
        self.is_vertex_of_rect = [[False] * len(self.arr[0]) for i in range(len(self.arr))]

    def start_random_split(self):
        self.split_rectangle([0, 0], [len(self.arr) - 1, len(self.arr[0]) - 1])

    def split_horizontally(self, pos0, pos1, new_pos):
        self.split_rectangle(pos0, [new_pos, pos1[1]])
        self.split_rectangle([new_pos + 1, pos0[1]], pos1)

    def split_vertical(self, pos0, pos1, new_pos):
        self.split_rectangle(pos0, [pos1[0], new_pos])
        self.split_rectangle([pos0[0], new_pos + 1], pos1)

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

        '''
        либо вертикальная, либо горизонатальная прямая
        '''
        if is_random_proc():
            self.split_horizontally(pos0, pos1, randint(min_pos[0], max_pos[0]))
        else:
            self.split_vertical(pos0, pos1, randint(min_pos[1], max_pos[1]))

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
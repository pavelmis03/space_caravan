from map.level.rect.graph_manager import RectGraphManager
from utils.disjoint_set import DisjointSet
from utils.random import is_random_proc


class RectUnioner:
    """
    делает из прямоугольников фигуры с углами 270 и 90 градусов,
    объединяя некоторые прямоугольники

    :return:
    """
    def __init__(self, arr, rects_count):
        self.arr = arr
        self.UNION_CHANCE = (len(self.arr) * len(self.arr[0])) ** (1 / 2)

        self.rect_graph = []
        RectGraphManager.save_rect_graph(self.arr, rects_count, self.rect_graph)

        self.figures_count = [1 for i in range(rects_count)]
        self.dis_set = DisjointSet(rects_count)

    def start_random_union(self):
        """
        Проходится по всем ребрам графа (ребро есть, если прямоугольники граничат).

        с некоторой вероятностью объединяет прямоугольники.
        :return:
        """
        for i in range(len(self.rect_graph)):
            for j in self.rect_graph[i]:
                chance = self.get_union_chance(i, j)
                if is_random_proc(chance):
                    self.union_rects(i, j)

    def union_rects(self, rect_num1, rect_num2):
        self.dis_set.union(rect_num1, rect_num2)
        new_figure_count = self.figures_count[rect_num1] + \
                           self.figures_count[rect_num2]

        self.figures_count[rect_num1] = new_figure_count
        self.figures_count[rect_num2] = new_figure_count

    def get_union_chance(self, rect_num1: int, rect_num2: int) -> int:
        if self.dis_set.check(rect_num1, rect_num2):
            return 0

        new_figure_count = self.figures_count[rect_num1] * \
                            self.figures_count[rect_num2]

        return int(self.UNION_CHANCE // (new_figure_count ** 2))

    def delete_edges(self):
        """
        удаляет клетки, которые разделяют
        прямоугольники одной фигуры.
        :return:
        """
        self.change_colors_of_same_figures()
        dy = [-1, -1, 0, 1, 1, 1, 0, -1]
        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        for i in range(1, len(self.arr) - 1):
            for j in range(1, len(self.arr[i]) - 1):
                if self.arr[i][j]:
                    continue

                has_other_cells = False
                cell_color = 0
                for k in range(len(dy)):
                    new_i = i + dy[k]
                    new_j = j + dx[k]
                    if not self.arr[new_i][new_j]:
                        continue
                    if not cell_color:
                        cell_color = self.arr[new_i][new_j]
                    elif cell_color != self.arr[new_i][new_j]:
                        has_other_cells = True
                        break
                """
                если стена граничит только с другими стенами или 
                клетками одной и той же фигуры, то ее следует удалить
                """
                if not has_other_cells:
                    self.arr[i][j] = cell_color

    def change_colors_of_same_figures(self):
        for i in range(1, len(self.arr) - 1):
            for j in range(1, len(self.arr[i]) - 1):
                if self.arr[i][j]:
                    self.arr[i][j] = self.dis_set.get_parent(self.arr[i][j])
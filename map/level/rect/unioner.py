from map.level.rect.graph.manager import RectGraphManager
from utils.disjoint_set import DisjointSet
from utils.random import is_random_proc


class RectUnioner:
    """
    делает из прямоугольников фигуры с углами 270 и 90 градусов,
    объединяя некоторые прямоугольники
    """

    def __init__(self, graph_manager: RectGraphManager):
        self.arr = graph_manager.arr
        self.UNION_CHANCE = (len(self.arr) * len(self.arr[0])) ** (1 / 2)

        self.rect_graph = []
        graph_manager.save_rect_graph(self.rect_graph)

        self.figures_count = [1 for i in range(graph_manager.rects_count)]
        self.dis_set = DisjointSet(graph_manager.rects_count)

    def start_random_union(self):
        """
        Проходится по всем ребрам графа (ребро есть, если прямоугольники граничат).

        с некоторой вероятностью UNION_CHANCE объединяет прямоугольники.
        """
        for i in range(len(self.rect_graph)):
            for j in self.rect_graph[i]:
                chance = self.__get_union_chance(i, j)
                if is_random_proc(chance):
                    self.__union_figures(i, j)

    def __union_figures(self, rect_num1, rect_num2):
        """
        Объединение фигур (которые могут быть уже не прямоугольниками)
        """
        self.dis_set.union(rect_num1, rect_num2)
        new_figure_count = self.figures_count[rect_num1] + \
            self.figures_count[rect_num2]

        self.figures_count[rect_num1] = new_figure_count
        self.figures_count[rect_num2] = new_figure_count

    def __get_union_chance(self, rect_num1: int, rect_num2: int) -> int:
        """
        Получить вероятность объединения фигур. Если они представляют собой уже объединенные прямоугольники, шанс ниже.
        """
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
        self.__change_colors_of_same_figures()
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

    def __change_colors_of_same_figures(self):
        """
        Делает внутри одной фигуры, состоящей из какого-то количества прямоугольников), одинаковый цвет.
        """
        for i in range(1, len(self.arr) - 1):
            for j in range(1, len(self.arr[i]) - 1):
                if self.arr[i][j]:
                    self.arr[i][j] = self.dis_set.get_parent(self.arr[i][j])

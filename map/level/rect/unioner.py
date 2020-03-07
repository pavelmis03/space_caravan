from map.level.rect.graph_manager import RectGraphManager
from utils.disjoint_set import DisjointSet
from utils.random import is_random_proc


class RectUnioner:
    """
    делает из прямоугольников фигуры с углами 270 и 90 градусов,
    объединяя некоторые прямоугольники

    :return:
    """
    def __init__(self, arr, is_vertex_of_rect, rects_count):
        self.arr = arr
        self.UNION_CHANCE = (len(self.arr) * len(self.arr[0])) ** (1 / 2)

        self.rect_graph = []
        RectGraphManager.save_rect_graph(self.arr, is_vertex_of_rect, rects_count, self.rect_graph)

        self.figures_count = [1 for i in range(rects_count)]
        self.dis_set = DisjointSet(rects_count)

    def start_random_union(self):
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

        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                if self.arr[i][j]:
                    self.arr[i][j] = self.dis_set.get_parent(self.arr[i][j])

        dy = [-1, -1, 0, 1, 1, 1, 0, -1]
        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        for i in range(1, len(self.arr) - 1):
            for j in range(1, len(self.arr[i]) - 1):
                if not self.arr[i][j]:
                    continue

                has_other_cells = False
                for k in range(len(dy)):
                    new_i = i + dy[k]
                    new_j = j + dx[k]
                    if self.arr[new_i][new_j] and \
                        self.arr[i][j] != self.arr[new_i][new_j]:
                        has_other_cells = True
                        break

                """
                если клетка не граничит с клетками другой фигуры,
                то эта клетка внутренняя, и она подлежит удалению
                """
                if not has_other_cells:
                    self.arr[i][j] = 0
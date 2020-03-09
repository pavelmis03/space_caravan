from typing import List

class Edge:
    def __init__(self, i1, j1, i2, j2, arr):
        self.i = [i1, i2]
        self.j = [j1, j2]
        self.color = [arr[i1][j1], arr[i2][j2]]
    def delete(self, arr):
        '''
        Стена лежит между i[0]j[0] и i[1]j[1]
        :param arr:
        :return:
        '''
        i, j = self.i, self.j
        wall_i = i[0] + (i[1] - i[0]) // 2
        wall_j = j[0] + (j[1] - j[0]) // 2

        arr[wall_i][wall_j] = self.color[0]

class RectGraphManager:
    dy = [-1, 0]
    dx = [0, -1]
    """
    Чтобы не дублировать ребра, проверяются только
    ребра из клетки влево и из клетки вверх
    """
    @staticmethod
    def save_rect_graph(arr, r_count, res):
        """
        Ребро означает наличие непосредственного
        контакта двух прямоугольников. То есть прямоугольники - вершины,
        ребро есть, если прямоугольники граничат.

        Прямоугольники граничат, существует стена, по 1 сторону (либо по оси x, либо по оси у)
        от нее клетка прямоугольника одного цвета, а по другую (по той же оси) другого цвета.

        Например:
        102
        или
        1
        0
        2
        :param arr:
        :param is_vertex_of_rect:
        :param r_count:
        :param res:
        :return:
        """
        dy = RectGraphManager.dy
        dx = RectGraphManager.dx

        for i in range(r_count):
            res.append([])
        has_edge = [[0] * r_count for i in range(r_count)]
        for i in range(1, len(arr) - 1):
            for j in range(1, len(arr[i]) - 1):
                if arr[i][j]:
                    continue
                for k in range(len(dy)):
                    new1_i = i + dy[k]
                    new1_j = j + dx[k]

                    new2_i = i - dy[k]
                    new2_j = j - dx[k]

                    if not RectGraphManager.is_can_be_edge(new1_i, new1_j,
                                                           new2_i, new2_j, arr):
                        continue

                    c1 = arr[new1_i][new1_j]
                    c2 = arr[new2_i][new2_j]
                    if has_edge[c1][c2]:
                        continue
                    has_edge[c1][c2] = has_edge[c2][c1] = True
                    res[c1].append(c2)
                    res[c2].append(c1)


    @staticmethod
    def save_edges_between_rects(arr, res):
        """
        Вершины - клетки arr.
        Ребро - две клетки различных цветов (не 0).

        Две клетки составляют ребро, существует стена, по 1 сторону (либо по оси x, либо по оси у)
        от нее первая клетка, а по другую (по той же оси) вторая.
        Клетки 1 и 2 не ребра:
        144
        000
        332
        :param arr:
        :param is_vertex_of_rect:
        :param res:
        :return:
        """
        dy = RectGraphManager.dy
        dx = RectGraphManager.dx

        for i in range(1, len(arr) - 1):
            for j in range(1, len(arr[i]) - 1):
                for k in range(len(dy)):
                    new1_i = i + dy[k]
                    new1_j = j + dx[k]

                    new2_i = i - dy[k]
                    new2_j = j - dx[k]
                    if not RectGraphManager.is_can_be_edge(new1_i, new1_j,
                                                           new2_i, new2_j, arr):
                        continue

                    res.append(Edge(new1_i, new1_j, new2_i, new2_j, arr))

    @staticmethod
    def is_can_be_edge(new1_i: int, new1_j: int, new2_i: int, new2_j: int,
                       arr: List[bool]) -> bool:
        return (arr[new1_i][new1_j] and arr[new2_i][new2_j] and
                        arr[new1_i][new1_j] != arr[new2_i][new2_j])


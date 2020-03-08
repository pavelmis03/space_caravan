from typing import List

class Edge:
    def __init__(self, i1, j1, i2, j2, arr):
        self.i = [i1, i2]
        self.j = [j1, j2]
        self.color = [arr[i1][j1], arr[i2][j2]]
    def delete(self, arr):
        i, j = self.i, self.j
        arr[i[0]][j[0]], arr[i[1]][j[1]] = 0, 0

class RectGraphManager:
    dy = [-1, 0]
    dx = [0, -1]
    """
    Чтобы не дублировать ребра, проверяются только
    ребра из клетки влево и из клетки вверх
    """
    @staticmethod
    def save_rect_graph(arr, is_vertex_of_rect, r_count, res):
        """
        Ребро означает наличие непосредственного
        контакта двух прямоугольников. То есть прямоугольники - вершины,
        ребро есть, если прямоугольники граничат.

        Прямоугольники граничат,
        если какие-то 2 клетки их сторон граничат (вершины прямоугольников не считаются).

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
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if not arr[i][j]:
                    continue
                for k in range(len(dy)):
                    new_i = i + dy[k]
                    new_j = j + dx[k]

                    if not RectGraphManager.is_can_be_edge(i, j, new_i, new_j,
                            arr, is_vertex_of_rect):
                        continue

                    c1 = arr[i][j]
                    c2 = arr[new_i][new_j]
                    if has_edge[c1][c2]:
                        continue
                    has_edge[c1][c2] = has_edge[c2][c1] = True
                    res[c1].append(c2)
                    res[c2].append(c1)
    @staticmethod
    def save_edges_between_rects(arr, is_vertex_of_rect, res):
        """
        Вершины - клетки arr.
        Ребро - две клетки различных цветов, которые не
        являются вершинами прямоугольника.

        :param arr:
        :param is_vertex_of_rect:
        :param res:
        :return:
        """
        dy = RectGraphManager.dy
        dx = RectGraphManager.dx

        for i in range(len(arr)):
            for j in range(len(arr[i])):
                for k in range(len(dy)):
                    new_i = i + dy[k]
                    new_j = j + dx[k]

                    if not RectGraphManager.is_can_be_edge(i, j, new_i, new_j,
                            arr, is_vertex_of_rect):
                        continue

                    res.append(Edge(i, j, new_i, new_j, arr))

    @staticmethod
    def is_can_be_edge(i: int, j: int, new_i: int, new_j: int,
                       arr, is_vertex_of_rect: List[bool]) -> bool:
        if new_i < 0 or new_j < 0:
            return False

        if not (arr[i][j] and arr[new_i][new_j]):
            return False  # 0 - внутренняя часть rect

        if is_vertex_of_rect[i][j] or \
                is_vertex_of_rect[new_i][new_j]:
            return False

        return arr[i][j] != arr[new_i][new_j]

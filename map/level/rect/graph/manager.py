from typing import List, Dict

from map.level.rect.graph.edge import Edge, EdgeManager

class RectGraphSaver:
    """
    Класс, формирующий граф между прямоугольниками
    """
    def __init__(self, rects_count: int, res: List[List[int]]):
        self.res = res
        for i in range(rects_count):
            self.res.append([])
        self.has_edge = [[False] * rects_count for i in range(rects_count)]

    def manage_edge(self, edge_manager: EdgeManager, connects: List[List[Dict[str, int]]],
                    direction: List[int], arr: List[List[int]]):
        """
        Добавить ребро между прямоугольниками, если его еще нет.
        """
        new1 = connects[0][0]
        new2 = connects[1][0]
        color1 = arr[new1['i']][new1['j']]
        color2 = arr[new2['i']][new2['j']]
        if self.has_edge[color1][color2]:
            return
        self.has_edge[color1][color2] = True
        self.res[color1].append(color2)
        self.res[color2].append(color1)

class EdgeSaver:
    """
    Класс, сохраняющий ребра (проходы).
    """
    def __init__(self, res: List[Edge]):
        self.res = res
    def manage_edge(self, edge_manager: EdgeManager, connects: List[List[Dict[str, int]]],
                    direction: List[int], arr: List[List[int]]):
        """
        Создает ребро (по связям и направлению) и добавляет.
        """
        edge_manager.create_edge(connects, direction, self.res)

class RectGraphManager:
    dy = [-1, 0]
    dx = [0, -1]
    """
    Чтобы не дублировать ребра, проверяются только
    ребра из клетки влево и из клетки вверх
    """
    def __init__(self, arr: List[List[int]], rects_count: int):
        self.arr = arr
        self.rects_count = rects_count
    def save_rect_graph(self, res: List[List[int]]):
        """
        Сохранить граф прямоугольников.

        Если прямоугольники граничат, то между ними есть ребро.
        """
        rect_graph_saver = RectGraphSaver(self.rects_count, res)
        self.manage_all_edges(rect_graph_saver)

    def save_edges_between_rects(self, res):
        """
        Сохранить все ребра
        """
        edges_saver = EdgeSaver(res)
        self.manage_all_edges(edges_saver)

    def manage_all_edges(self, res_saver):
        """
        Вершины - клетки arr.
        Ребро - две группы клеток различных фигур, между которыми стены.
        :param arr:
        :param is_vertex_of_rect:
        :param res:
        :return:
        """
        dy = RectGraphManager.dy
        dx = RectGraphManager.dx
        self.used = [[False] * len(self.arr[0]) for i in range(len(self.arr))]
        edge_manager = EdgeManager(self.arr, self.used)

        for i in range(1, len(self.arr) - 1):
            for j in range(1, len(self.arr[i]) - 1):
                if self.arr[i][j]:
                    continue
                for k in range(len(dy)):
                    connects = [[], []]

                    if not edge_manager.try_create_connects(i, j, dy[k], dx[k], connects):
                        continue

                    if not edge_manager.can_create_edge(connects):
                        continue

                    res_saver.manage_edge(edge_manager, connects, [dx[k], dy[k]], self.arr)
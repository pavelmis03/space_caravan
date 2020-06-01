from typing import List
from geometry.point import Point
from geometry.rectangle import Rectangle
from geometry.optimized.segment import StaticSegment


class StaticRectangle(Rectangle):
    """
    Статический прямоугольник. Его точки нельзя менять. За счет этого можно получить некоторый бонус в
    производительности, т.к. некоторые значения можно предподсчитать.
    """

    def __init__(self, left_x: float = 0, up_y: float = 0, right_x: float = 0, down_y: float = 0):
        super().__init__(left_x, up_y, right_x, down_y)
        self._vertexes = super().get_vertexes()

        old_edges = super().get_edges()
        self._edges = []
        for i in range(len(old_edges)):
            self._edges.append(StaticSegment(old_edges[i].p1, old_edges[i].p2))

    def get_vertexes(self) -> List[Point]:
        """
        :return: список вершин прямоугольника
        """
        return self._vertexes

    def get_edges(self) -> List[StaticSegment]:
        """
        :return: список статических отрезков
        """
        return self._edges

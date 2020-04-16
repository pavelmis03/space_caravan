from typing import List
from geometry.point import Point
from geometry.rectangle import Rectangle
from geometry.optimized.segment import StaticSegment

class StaticRectangle(Rectangle):
    def __init__(self, left_x: float = 0, up_y: float = 0, right_x: float = 0, down_y: float = 0):
        super().__init__(left_x, up_y, right_x, down_y)
        self._vertexes = super().get_vertexes()

        self._edges = super().get_edges()
        for i in range(len(self._edges)):
            self._edges[i] = StaticSegment(self._edges[i].p1, self._edges[i].p2)

    def get_vertexes(self) -> List[Point]:
        return self._vertexes

    def get_edges(self) -> List[StaticSegment]:
        return self._edges
from geometry.point import Point
from geometry.segment import Segment

def get_vector(first: Point, second: Point) -> Point:
    return Point(second.x - first.x, second.y - first.y)

class StaticSegment(Segment):
    def __init__(self, p1: Point, p2: Point):
        super().__init__(p1, p2)
        self._length = super().length

        self.min_x = min(p1.x, p2.x)
        self.max_x = max(p1.x, p2.x)

        self.min_y = min(p1.y, p2.y)
        self.max_y = max(p1.y, p2.y)

        self.vector = get_vector(self.p1, self.p2)

    @property
    def length(self):
        return self._length
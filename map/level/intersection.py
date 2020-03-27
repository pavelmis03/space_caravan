from map.level.grid_path_finder import IsMarkedManager
from geometry.segment import Segment
from geometry.intersections import intersect_seg_rect
from collections import deque
from constants.directions import side_di, side_dj

class GridIntersectionManager:
    def __init__(self, grid):
        self.grid = grid
        self.used_manager = IsMarkedManager(grid.arr)

    def is_segment_intersect_walls(self, seg: Segment) -> bool:
        self.used_manager.next_iteration()
        i0, j0 = self.grid.index_manager.get_index_by_pos(seg.p1)

        s = deque()
        self.used_manager.mark(i0, j0)
        s.append((i0, j0))

        while (len(s)):
            i, j = s.pop()
            for k in range(len(side_di)):
                new_i = i + side_di[k]
                new_j = j + side_dj[k]
                if self.used_manager.is_marked(new_i, new_j):
                    continue
                rect = self.grid.get_collision_rect(new_i, new_j)
                if intersect_seg_rect(seg, rect) is None:
                    continue

                if not self.grid.is_passable(new_i, new_j):
                    return True

                self.used_manager.mark(new_i, new_j)
                s.append((new_i, new_j))

            if i == i0 and j == j0 and not len(s):
                for k in range(len(side_di)):
                    new_i = i + side_di[k]
                    new_j = j + side_dj[k]
                    if self.used_manager.is_marked(new_i, new_j):
                        continue
                    rect = self.grid.get_collision_rect(new_i, new_j)
                    print(rect.top_left.x)
                    print(rect.bottom_right.x)
                    print(rect.top_left.y)
                    print(rect.bottom_right.y)
                    if intersect_seg_rect(seg, rect) is None:
                        continue

                    if not self.grid.is_passable(new_i, new_j):
                        return True

                    self.used_manager.mark(new_i, new_j)
                    s.append((new_i, new_j))

        return False


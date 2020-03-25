from typing import List, Tuple
from geometry.segment import Segment
from geometry.intersections import intersect_seg_rect
from collections import deque
from constants import di, dj
from drawable_objects.enemy import Enemy
from drawable_objects.base import GameSprite
from geometry.point import Point

class IsMarkedManager:
    def __init__(self, arr: List[List[int]]):
        self._marked = [[0] * len(arr[0]) for i in range(len(arr))]
        self._mark_counter = 1

    def next_iteration(self):
        self._mark_counter += 1

    def mark(self, i: int, j: int):
        self._marked[i][j] = self._mark_counter

    def is_marked(self, i: int, j: int) -> bool:
        return (self._marked[i][j] == self._mark_counter)


class GridPathFinder:
    def __init__(self, grid):
        self.grid = grid

        self.distance = [[0] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.used_manager = IsMarkedManager(grid.arr)

        self.enemy_exist = IsMarkedManager(grid.arr)
        self.enemies_matrix = [[None] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.parent = [[0, 0] * len(grid.arr[0]) for i in range(len(grid.arr))]

    def add_enemy(self, enemy: Enemy):
        i, j = self.grid.index_manager.get_index_by_pos(enemy.pos)
        self.enemy_exist.mark(i, j)
        self.enemies_matrix[i][j] = enemy

    def find_path_to_enemies(self, max_distance: int) -> List[Tuple[int, int]]:
        self.used_manager.next_iteration()
        player_pos = self.grid.scene.player.pos
        player_i, player_j = self.grid.index_manager.get_index_by_pos(player_pos)
        q = deque()
        q.append((player_i, player_j))
        self.distance[player_i][player_j] = 0
        self.used_manager.mark(player_i, player_j)

        enemies_in_range = []

        while len(q):
            i, j = q.popleft()

            if self.enemy_exist.is_marked(i, j):
                enemies_in_range.append((i, j))

            new_distance = self.distance[i][j] + 1
            if new_distance > max_distance:
                continue

            for k in range(len(di)):
                new_i = i + di[k]
                new_j = j + dj[k]

                if self.used_manager.is_marked(new_i, new_j) or \
                        not self.grid.is_passable(new_i, new_j):
                    continue

                self.used_manager.mark(new_i, new_j)
                self.parent[new_i][new_j] = (i, j)
                self.distance[new_i][new_j] = new_distance

                q.append((new_i, new_j))

        self.enemy_exist.next_iteration()

        return enemies_in_range

    def is_segment_intersect_walls(self, seg: Segment) -> bool:
        self.used_manager.next_iteration()
        i0, j0 = self.grid.index_manager.get_index_by_pos(seg.p1)

        s = deque()
        self.used_manager.mark(i0, j0)
        s.append((i0, j0))
        self.grid.scene.delete_me_later = []
        while (len(s)):
            i, j = s.pop()
            gs = GameSprite(self.grid.scene, self.grid.controller,
                           'green', Point(j * self.grid.cell_width + self.grid.cell_width / 2,
                                          i * self.grid.cell_height + self.grid.cell_height / 2))
            self.grid.scene.delete_me_later.append(gs)
            for k in range(len(di)):
                new_i = i + di[k]
                new_j = j + dj[k]
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
                for k in range(len(di)):
                    new_i = i + di[k]
                    new_j = j + dj[k]
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
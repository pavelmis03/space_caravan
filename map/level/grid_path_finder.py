from typing import List, Tuple
from geometry.segment import Segment
from geometry.intersections import intersect_seg_rect
from collections import deque
from constants import side_di, side_dj, diagonal_di, diagonal_dj
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

        self.parent = [[(0, 0)] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.can_stay = [[True] * len(grid.arr[i]) for i in range(len(grid.arr))]

        for i in range(1, len(self.grid.arr) - 1):
            for j in range(1, len(self.grid.arr[i]) - 1):
                if not self.grid.is_passable(i, j):
                    self.can_stay[i][j] = False
                    continue
                for k in range(len(side_di)):
                    new_i = i + side_di[k]
                    new_j = j + side_dj[k]
                    if not self.grid.is_passable(new_i, new_j):
                        self.can_stay[i][j] = False
                        break

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

            for k in range(len(side_di)):
                new_i = i + side_di[k]
                new_j = j + side_dj[k]

                if self.used_manager.is_marked(new_i, new_j) or \
                        not self.grid.is_passable(new_i, new_j):
                    continue

                self.used_manager.mark(new_i, new_j)
                self.parent[new_i][new_j] = (i, j)
                self.distance[new_i][new_j] = new_distance

                q.append((new_i, new_j))

        self.enemy_exist.next_iteration()

        return enemies_in_range

    def get_point_to_move(self, enemy: Enemy) -> Point:
        i, j = self.grid.index_manager.get_index_by_pos(enemy.pos)
        if not self.used_manager.is_marked(i, j):
            return None

        player_pos = self.grid.scene.player.pos
        player_i, player_j = self.grid.index_manager.get_index_by_pos(player_pos)
        path = []
        p = (i, j)
        while p != (player_i, player_j):
            path.append(p)
            p = self.parent[p[0]][p[1]]

        path.append((player_i, player_j))

        l = 0
        r = len(path)
        while r - l > 1:
            m = (l + r) // 2
            pos = self.grid.index_manager.get_center_of_cell_by_indexes(path[m][0], path[m][1])
            if self.is_segment_intersect_walls(Segment(enemy.pos, pos)):
                r = m
            else:
                l = m

        return self.grid.index_manager.get_center_of_cell_by_indexes(path[l][0], path[l][1])

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
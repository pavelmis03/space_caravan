from typing import List, Tuple
from geometry.point import Point
from drawable_objects.enemy import Enemy
from collections import deque
from constants import di, dj
from geometry.vector import length
from geometry.segment import Segment
from geometry.rectangle import Rectangle
from geometry.intersections import intersect_seg_rect

class GridPathManager:
    """
    Возможны ошибки:
    если два enemy в одной клетке
    если enemy в клетке с player
    """
    def __init__(self, grid):
        self.grid = grid

        self.used = [[0] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.distance = [[0] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.enemy_exist = [[0] * len(grid.arr[0]) for i in range(len(grid.arr))]
        self.enemies_matrix = [[None] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.parent = [[0, 0] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.enemies = []

        self.iteration_counter = 1
        self.used_counter = 1

    def add_enemy_in_matrix(self, enemy: Enemy):
        i, j = self.grid.index_manager.get_index_by_pos(enemy.pos)
        self.enemy_exist[i][j] = self.iteration_counter
        self.enemies_matrix[i][j] = enemy

    def add_enemy_in_list(self, enemy: Enemy):
        dt = self.grid.scene.player.pos - enemy.pos
        if length(dt) <= Enemy.VISION_RADIUS:
            self.enemies.append(enemy)

    def set_enemy_in_arr(self, enemy: Enemy):
        self.add_enemy_in_matrix(enemy)
        self.add_enemy_in_list(enemy)

    def get_enemies_in_vision_radius(self, player_pos: Point) -> List[Tuple[int, int]]:
        self.used_counter += 1
        player_i, player_j = self.grid.index_manager.get_index_by_pos(player_pos)
        """
        используем deque т.к. он работает не медленнее queue 
        """
        q = deque()
        q.append((player_i, player_j))
        self.distance[player_i][player_j] = 0
        self.used[player_i][player_j] = self.used_counter

        result = []

        while len(q):
            i, j = q.popleft()

            if self.enemy_exist[i][j] == self.iteration_counter:
                result.append((i, j))

            new_distance = self.distance[i][j] + 1
            if new_distance > Enemy.HEARING_RANGE:
                continue

            for k in range(len(di)):
                new_i = i + di[k]
                new_j = j + dj[k]

                if self.used[new_i][new_j] == self.used_counter or \
                    not self.grid.is_passable(new_i, new_j):
                    continue

                self.used[new_i][new_j] = self.used_counter
                self.parent[new_i][new_j] = (i, j)
                self.distance[new_i][new_j] = new_distance

                q.append((new_i, new_j))

        self.iteration_counter += 1

        return result

    def path_finding(self):
        enemies_indexes = self.get_enemies_in_vision_radius(self.grid.scene.player.pos)
        for i in range(len(enemies_indexes)):
            self.enemies_matrix[enemies_indexes[i][0]][enemies_indexes[i][1]].recount_angle()

    def is_segment_intersect_walls(self, seg: Segment) -> bool:
        self.used_counter += 1
        i0, j0 = self.grid.index_manager.get_index_by_pos(seg.p1)

        s = deque()
        self.used[i0][j0] = self.used_counter
        s.append((i0, j0))
        while (len(s)):
            i, j = s.pop()
            for k in range(len(di)):
                new_i = i + di[k]
                new_j = j + dj[k]
                if self.used[new_i][new_j] == self.used_counter:
                    continue
                rect = self.grid.get_collision_rect(new_i, new_j)
                if intersect_seg_rect(seg, rect) is None:
                    continue

                if not self.grid.is_passable(new_i, new_j):
                    return True

                self.used[new_i][new_j] = self.used_counter
                s.append((new_i, new_j))

        return False

    def enemies_vision_logic(self):
        for i in range(len(self.enemies)):
            seg = Segment(self.enemies[i].pos, self.grid.scene.player.pos)
            if self.is_segment_intersect_walls(seg):
                continue
            self.enemies[i].recount_angle()
        self.enemies = []

    def process_logic(self):
        self.enemies_vision_logic()
        pass
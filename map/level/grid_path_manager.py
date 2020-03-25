from typing import List, Tuple
from geometry.point import Point
from drawable_objects.enemy import Enemy
from collections import deque
from constants import di, dj

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
        self.enemies = [[0] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.parent = [[0, 0] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.iteration_counter = 1

    def set_enemy_in_arr(self, enemy: Enemy):
        i, j = self.grid.index_manager.get_index_by_pos(enemy.pos)
        self.enemy_exist[i][j] = self.iteration_counter
        self.enemies[i][j] = enemy

    def get_enemies_in_vision_radius(self, player_pos: Point) -> List[Tuple[int, int]]:
        player_i, player_j = self.grid.index_manager.get_index_by_pos(player_pos)
        """
        используем deque т.к. он работает не медленнее queue 
        """
        q = deque()
        q.append((player_i, player_j))
        self.distance[player_i][player_j] = 0
        self.used[player_i][player_j] = self.iteration_counter

        result = []

        while len(q):
            i, j = q.popleft()

            if self.enemy_exist[i][j] == self.iteration_counter:
                result.append((i, j))

            new_distance = self.distance[i][j] + 1
            if new_distance > Enemy.VISION_RADIUS:
                continue

            for k in range(len(di)):
                new_i = i + di[k]
                new_j = j + dj[k]

                if self.used[new_i][new_j] == self.iteration_counter or \
                    not self.grid.is_passable(new_i, new_j):
                    continue

                self.used[new_i][new_j] = self.iteration_counter
                self.parent[new_i][new_j] = (i, j)
                self.distance[new_i][new_j] = new_distance

                q.append((new_i, new_j))

        self.iteration_counter += 1

        return result

    def path_finding(self):
        enemies_indexes = self.get_enemies_in_vision_radius(self.grid.scene.player.pos)
        for i in range(len(enemies_indexes)):
            self.enemies[enemies_indexes[i][0]][enemies_indexes[i][1]].recount_angle()

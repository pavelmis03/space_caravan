from collections import deque
from typing import List, Tuple

from constants.directions import rect_di, rect_dj
from drawable_objects.enemy import Enemy
from geometry.point import Point
from utils.is_marked_manager import IsMarkedManager


class GridPathFinder:
    """
    Обход двумерного графа. Поиск пути (bfs).
    """
    def __init__(self, grid):
        """
        O(len(grid.arr) * len(grid.arr[0])) памяти и времени
        """
        self.grid = grid

        self.distance = [[0] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.used_manager = IsMarkedManager(grid.arr)

        self.parent = [[(0, 0)] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.can_stay = [[True] * len(grid.arr[i]) for i in range(len(grid.arr))]

        self.fill_can_stay_array()

    def fill_can_stay_array(self):
        """
        O(len(grid.arr) * len(grid.arr[0])) времени

        can stay если клетка не стена и соседняя тоже.
        """
        for i in range(len(self.grid.arr)):
            for j in range(len(self.grid.arr[i])):
                if not self.grid.is_passable(i, j):
                    self.can_stay[i][j] = False
                    continue
                for k in range(len(rect_di)):
                    new_i = i + rect_di[k]
                    new_j = j + rect_dj[k]
                    if not self.grid.is_passable(new_i, new_j):
                        self.can_stay[i][j] = False
                        break

    def get_standable_cells(self, i0: int, j0: int) -> List[Tuple[int, int]]:
        """
        O(len(rect_di)) == O(1) времени
        """
        result = []
        for k in range(len(rect_di)):
            new_i = i0 + rect_di[k]
            new_j = j0 + rect_dj[k]

            if self.can_stay[new_i][new_j]:
                result.append((new_i, new_j))

        return result

    def update_path_to_enemies(self, max_distance: int):
        """
        запускает всего один bfs от игрока, а не от каждого enemy.
        игнорирует клетки, которые не can_stay
        """
        self.used_manager.next_iteration()
        player_pos = self.grid.scene.player.pos
        player_i, player_j = self.grid.index_manager.get_index_by_pos(player_pos)
        q = deque()
        q.append((player_i, player_j))
        self.distance[player_i][player_j] = 0
        self.used_manager.mark(player_i, player_j)

        while len(q):
            i, j = q.popleft()

            new_distance = self.distance[i][j] + 1
            if new_distance > max_distance:
                continue

            transition_cells = self.get_standable_cells(i, j)
            for k in range(len(transition_cells)):
                new_i = transition_cells[k][0]
                new_j = transition_cells[k][1]

                if self.used_manager.is_marked(new_i, new_j):
                    continue

                self.used_manager.mark(new_i, new_j)
                self.parent[new_i][new_j] = (i, j)
                self.distance[new_i][new_j] = new_distance

                q.append((new_i, new_j))

    def get_pos_to_move(self, enemy: Enemy) -> Point:
        """
        O(1) времени

        Важно понимать, что Enemy ходит по клеткам, а не ищет кратчайший путь.
        Это сильно экономит производительность, но может выглядеть топорно.
        """
        i, j = self.grid.index_manager.get_index_by_pos(enemy.pos)

        if not self.used_manager.is_marked(i, j):
            return None

        new_i, new_j = self.parent[i][j]

        return self.grid.get_center_of_cell_by_indexes(new_i, new_j)




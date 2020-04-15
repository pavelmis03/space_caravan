from collections import deque
from typing import List, Tuple

from constants.directions import rect_di, rect_dj
from drawable_objects.enemy import Enemy
from geometry.point import Point
from utils.is_marked_manager import TwoDimensionalIsMarkedManager


class GridPathFinder:
    """
    Обход двумерного графа. Поиск пути (bfs).
    """
    def __init__(self, grid):
        """
        O(len(grid.arr) * len(grid.arr[0])) памяти и времени
        """
        self._grid = grid

        self._distance = [[0] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self._used_manager = TwoDimensionalIsMarkedManager(grid.arr)

        self._parent = [[(0, 0)] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self._can_stay = [[True] * len(grid.arr[i]) for i in range(len(grid.arr))]

        self._fill_can_stay_list()

    def _fill_can_stay_list(self):
        """
        Заполняет список can_stay

        O(len(grid.arr) * len(grid.arr[0])) времени

        can stay если клетка не стена и соседняя тоже.
        """
        for i in range(len(self._grid.arr)):
            for j in range(len(self._grid.arr[i])):
                if not self._grid.is_passable(i, j):
                    self._can_stay[i][j] = False
                    continue
                for k in range(len(rect_di)):
                    new_i = i + rect_di[k]
                    new_j = j + rect_dj[k]
                    if not self._grid.is_passable(new_i, new_j):
                        self._can_stay[i][j] = False
                        break

    def _get_standable_cells(self, i0: int, j0: int) -> List[Tuple[int, int]]:
        """
        Получить клетки, на которые Enemy может вставать.

        O(len(rect_di)) == O(1) времени
        """
        result = []
        for k in range(len(rect_di)):
            new_i = i0 + rect_di[k]
            new_j = j0 + rect_dj[k]

            if self._can_stay[new_i][new_j]:
                result.append((new_i, new_j))

        return result

    def _update_path_to_enemies(self, max_distance: int):
        """
        Обновляет путь от игрока до всех клеток, в рендже max_distance

        запускает всего один bfs от игрока, а не от каждого enemy. игнорирует клетки, которые не can_stay
        """
        self._used_manager.next_iteration()
        player_pos = self._grid.scene.player.pos
        player_i, player_j = self._grid.index_manager.get_index_by_pos(player_pos)
        q = deque()
        q.append((player_i, player_j))
        self._distance[player_i][player_j] = 0
        self._used_manager.mark(player_i, player_j)

        while len(q):
            i, j = q.popleft()

            new_distance = self._distance[i][j] + 1
            if new_distance > max_distance:
                continue

            transition_cells = self._get_standable_cells(i, j)
            for k in range(len(transition_cells)):
                new_i = transition_cells[k][0]
                new_j = transition_cells[k][1]

                if self._used_manager.is_marked(new_i, new_j):
                    continue

                self._used_manager.mark(new_i, new_j)
                self._parent[new_i][new_j] = (i, j)
                self._distance[new_i][new_j] = new_distance

                q.append((new_i, new_j))

    def get_pos_to_move(self, enemy: Enemy) -> Point:
        """
        Получить точку для движения.

        O(1) времени

        Важно понимать, что Enemy ходит по клеткам, а не ищет кратчайший путь.
        Это сильно экономит производительность, но может выглядеть топорно.
        """
        i, j = self._grid.index_manager.get_index_by_pos(enemy.pos)

        if not self._used_manager.is_marked(i, j):
            return None

        new_i, new_j = self._parent[i][j]

        return self._grid.get_center_of_cell_by_indexes(new_i, new_j)




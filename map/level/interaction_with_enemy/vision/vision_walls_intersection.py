from collections import deque
from typing import List, Tuple

from constants.directions import side_di, side_dj
from drawable_objects.enemy import Enemy
from utils.is_marked_manager import IsMarkedManager


class VisionWallsIntersection:
    """
    Следует использовать этот класс для обработки запросов
    вместо intersection_manager, так как работает в разы быстрее
    и сделан специально для enemy

    Обход двумерного графа (bfs). Отвечает на запрос, есть ли
    стены, мешающие увидеть вторую клетку из первой. Вторая клетка - клетка Player.
    """
    def __init__(self, grid):
        """
        O(len(grid.arr) * len(grid.arr[0])) памяти и времени
        """
        self.grid = grid

        self.distance = [[0] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.used_manager = IsMarkedManager(grid.arr)
        self.cant_see = IsMarkedManager(grid.arr)

    def is_see_player(self, enemy: Enemy) -> bool:
        """
        O(1) времени
        """
        i, j = self.grid.index_manager.get_index_by_pos(enemy.pos)
        return self.used_manager.is_marked(i, j) and not self.cant_see.is_marked(i, j)

    def get_standable_cells(self, i0: int, j0: int) -> List[Tuple[int, int]]:
        """
        O(1) времени

        НЕ может ходить по диагонали.
        Не выйдет за пределы поля.
        """
        result = []
        for k in range(len(side_di)):
            new_i = i0 + side_di[k]
            new_j = j0 + side_dj[k]

            if new_i < 0 or new_j < 0 or \
                new_i >= len(self.grid.arr) or new_j >= len(self.grid.arr[new_i]):
                continue
            result.append((new_i, new_j))

        return result

    def update_cant_see_to_enemies(self, max_distance: int):
        """
        запускает всего один bfs от игрока, а не от каждого enemy.

        v0 bfs - клетка Player, так как все проверяемые отрезки заканчиваются в клетке Player'а.
        bfs будет распространяться, игнорируя препятствия.
        Если хотя бы один предок вершины был стеной или она сама стена,
        то для этой вершины cant_see True, иначе False. (Причем если существует несколько
        кратчайших путей, то если в хотя бы одном из них была стена, то cant_see True)
        Если can_see True, то прямая, соединяющая эту клетку и клетку Player пересекает стену.

        Алгоритм неточен:
        когда из первой клетки нельзя увидеть вторую, всегда говорит cant_see True,
        но когда можно, в некоторых случаях говорит can_see True.
        """
        self.used_manager.next_iteration()
        self.cant_see.next_iteration()

        player_pos = self.grid.scene.player.pos
        player_i, player_j = self.grid.index_manager.get_index_by_pos(player_pos)
        q = deque()
        q.append((player_i, player_j))
        self.distance[player_i][player_j] = 0

        self.used_manager.mark(player_i, player_j)

        while len(q):
            i, j = q.popleft()
            if not self.grid.is_passable(i, j):
                self.cant_see.mark(i, j)

            if self.distance[i][j] > max_distance:
                continue
            new_distance = self.distance[i][j] + 1

            transition_cells = self.get_standable_cells(i, j)
            for k in range(len(transition_cells)):
                new_i = transition_cells[k][0]
                new_j = transition_cells[k][1]

                if self.used_manager.is_marked(new_i, new_j):
                    """
                    Важный if, без которого все сломается
                    (учитываем все кратчайшие пути).
                    """
                    if new_distance == self.distance[new_i][new_j] and \
                        self.cant_see.is_marked(i, j):
                            self.cant_see.mark(new_i, new_j)
                    continue

                self.used_manager.mark(new_i, new_j)
                self.distance[new_i][new_j] = new_distance
                if self.cant_see.is_marked(i, j):
                    self.cant_see.mark(new_i, new_j)

                q.append((new_i, new_j))
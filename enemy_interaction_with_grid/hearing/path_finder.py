from typing import List, Tuple, Optional
from collections import deque
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
        self.__grid = grid

        self.__distance = [[0] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.__used_manager = TwoDimensionalIsMarkedManager(grid.arr)

        self.__is_in_aggre_zone = TwoDimensionalIsMarkedManager(grid.arr)

        self.__parent = [[(0, 0)] * len(grid.arr[0]) for i in range(len(grid.arr))]

        self.__is_has_enemy = TwoDimensionalIsMarkedManager(grid.arr)

        # не мешают ли стены стоять здесь enemy
        self.__is_standable = [[True] * len(grid.arr[i]) for i in range(len(grid.arr))]

        self.__fill_is_standable_list()

    def __fill_is_standable_list(self):
        """
        Заполняет список __is_standable

        O(len(grid.arr) * len(grid.arr[0])) времени

        __is_standable если клетка не стена и соседняя тоже.
        """
        for i in range(len(self.__grid.arr)):
            for j in range(len(self.__grid.arr[i])):
                if not self.__grid.is_passable(i, j):
                    self.__is_standable[i][j] = False
                    continue
                for k in range(len(rect_di)):
                    new_i = i + rect_di[k]
                    new_j = j + rect_dj[k]
                    if not self.__grid.is_passable(new_i, new_j):
                        self.__is_standable[i][j] = False
                        break

    def update_path_to_enemies(self, max_distance: int):
        """
        Обновляет путь от игрока до всех клеток, в рендже max_distance

        запускает всего один bfs от игрока, а не от каждого enemy. игнорирует клетки, которые не can_stay
        """
        q = self.__main_bfs(max_distance)
        self.__aggre_zone_bfs(q, max_distance)

    def __aggre_zone_bfs(self, q: deque, max_distance: int):
        """
        Обработка клеток, из которых недостижим игрок, но которые находятся в aggre_zone
        (путь преграждает другой enemy)

        этот bfs похож на __main_bfs, но объединять общую часть кода не стоит, т.к. ухудшится
        читаемость кода.
        """
        self.__is_in_aggre_zone.next_iteration()

        while len(q):
            i, j = q.popleft()

            new_distance = self.__distance[i][j] + 1
            if new_distance > max_distance:
                continue

            transition_cells = self.__get_transition_cells(i, j)
            for k in range(len(transition_cells)):
                new_i = transition_cells[k][0]
                new_j = transition_cells[k][1]
                if self.__is_in_aggre_zone.is_marked(new_i, new_j): # уже обработано
                    continue

                self.__is_in_aggre_zone.mark(new_i, new_j) # важно, что тут не __used_manager
                self.__parent[new_i][new_j] = (i, j)
                self.__distance[new_i][new_j] = new_distance

                q.append((new_i, new_j))

    def __main_bfs(self, max_distance: int) -> deque:
        """
        Основной bfs, в котором обрабатываются пути от игрока до остальных клеток (и соответственно от остальных
        клеток до игрока).

        :return: deque клеток, которые недостижимы для enemy, но находится в aggre_zone
        """
        self.__used_manager.next_iteration()

        player_pos = self.__grid.scene.player.pos
        player_i, player_j = self.__grid.index_manager.get_index_by_pos(player_pos)

        q = deque()  # collections.deque работает быстрее, чем queue.Queue
        q.append((player_i, player_j))
        self.__distance[player_i][player_j] = 0

        in_aggre_zone = deque()

        while len(q):
            i, j = q.popleft()

            new_distance = self.__distance[i][j] + 1
            if new_distance > max_distance:
                continue

            transition_cells = self.__get_transition_cells(i, j)
            for k in range(len(transition_cells)):
                new_i = transition_cells[k][0]
                new_j = transition_cells[k][1]

                self.__used_manager.mark(new_i, new_j)
                self.__parent[new_i][new_j] = (i, j)
                self.__distance[new_i][new_j] = new_distance

                """
                клетки, на которых стоят enemy будут обработаны позже. Хоть на эти клетки не могут встать
                другие enemy, они находятся в aggre_zone.
                """
                if not self.__is_has_enemy.is_marked(i, j):
                    q.append((new_i, new_j))
                else:
                    in_aggre_zone.append((new_i, new_j))

        self.__is_has_enemy.next_iteration()
        return in_aggre_zone

    def __get_transition_cells(self, i0: int, j0: int) -> List[Tuple[int, int]]:
        """
        Получить клетки, на которые Enemy может вставать.

        O(len(rect_di)) == O(1) времени
        """
        result = []
        for k in range(len(rect_di)):
            new_i = i0 + rect_di[k]
            new_j = j0 + rect_dj[k]

            if self.__is_standable[new_i][new_j] and not self.__used_manager.is_marked(new_i, new_j):
                result.append((new_i, new_j))

        return result

    def can_stay(self, i: int, j: int) -> bool:
        """
        Может ли enemy стоять здесь.

        :return: True, если нет рядом стен и здесь не стоит уже другой enemy. Иначе False
        """
        return self.__is_standable[i][j] and not self.__is_has_enemy.is_marked(i, j)

    def save_enemy_pos(self, pos: Point):
        """
        Отмечает клетку, в которой стоит enemy, is_has_enemy
        """
        i, j = self.__grid.index_manager.get_index_by_pos(pos)
        self.__is_has_enemy.mark(i, j)

    def is_hearing_player(self, enemy: Enemy) -> bool:
        """
        Может ли услышать Enemy Player'а
        """
        i, j = self.__grid.index_manager.get_index_by_pos(enemy.pos)
        return self.__used_manager.is_marked(i, j)

    def is_in_aggre_zone(self, enemy: Enemy) -> bool:
        """
        находится ли enemy в зоне aggre игрока
        """
        i, j = self.__grid.index_manager.get_index_by_pos(enemy.pos)
        return self.__is_in_aggre_zone.is_marked(i, j) or self.__used_manager.is_marked(i, j)

    def get_pos_to_move(self, enemy: Enemy) -> Optional[Point]:
        """
        Получить точку для движения.

        O(1) времени

        Важно понимать, что Enemy ходит по клеткам, а не ищет кратчайший путь.
        Это сильно экономит производительность, но может выглядеть топорно.
        """
        i, j = self.__grid.index_manager.get_index_by_pos(enemy.pos)

        if not self.__used_manager.is_marked(i, j):
            return None

        new_i, new_j = self.__parent[i][j]

        """
        Отсутствие этого if'а может привести к багам. Например, enemy попадет в клетку, которая не is_standable и 
        останется там навсегда.
        """
        if not self.can_stay(new_i, new_j):
            return None

        return self.__grid.get_center_of_cell_by_indexes(new_i, new_j)




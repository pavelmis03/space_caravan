from typing import List, Tuple
from constants.directions import side_di, side_dj
from enemy_interaction_with_grid.vision.rectangle_bypass.rectangle_bypasser import RectangleBypasserAbstract
from map.level.rect.splitter import GridRectangle
from utils.list import is_indexes_correct


class RectangleNeighbours(RectangleBypasserAbstract):
    """
    Класс для поиска соседних комнат для данной.

    Различает соседей только по следующим категориям: верхний, правый, левый, нижний (относительно исходной комнаты).
    """
    neighbour_di = side_di
    neighbour_dj = side_dj
    def __init__(self, grid_rectangle: GridRectangle):
        super().__init__(grid_rectangle)
        self._top_neighbours = []
        self._right_neighbours = []
        self._bottom_neighbours = []
        self._left_neighbours = []

        self._all_neighbours = (self._top_neighbours, self._right_neighbours,
                                self._bottom_neighbours, self._left_neighbours)

    def get_neighbours(self, arr: List[List[int]], grid) -> \
                Tuple[List[int], List[int], List[int], List[int]]:
        """
        Возвращает списки Rectangle, к которым можно перейти
        из данного. Порядок списков Rectangle: верхний, правый, нижний, левый.
        """
        self._bypass(arr, grid)
        return self._all_neighbours

    def _handle_cell(self, cycle: int, i: int, j: int,
                      arr: List[List[int]], grid) -> bool:
        """
        Обработка клетки. По ней определяются соседи комнаты.
        """
        neighbour_cell_i = i + RectangleNeighbours.neighbour_di[cycle]
        neighbour_cell_j = j + RectangleNeighbours.neighbour_dj[cycle]

        if self._is_should_stop_bypass(arr, neighbour_cell_i, neighbour_cell_j):
            return False

        self._neighbour_logic(arr, cycle, neighbour_cell_i, neighbour_cell_j)

        return True

    def _neighbour_logic(self, arr, cycle, new_i, new_j):
        """
        Определяет neighbour по клетке. Добавляет neighbour в список, если это необходимо.
        """
        new_neighbour_color = arr[new_i][new_j]
        neighbours_list = self._all_neighbours[cycle]

        if self._is_should_add_neighbour(neighbours_list, new_neighbour_color):
            neighbours_list.append(new_neighbour_color)

    def _is_should_stop_bypass(self, arr: List[List[int]], new_i: int, new_j: int) -> bool:
        """
        если индексы некорректные, то они уже не станут корректными
        в силу прямоугольности сетки
        """
        return not is_indexes_correct(arr, new_i, new_j)

    def _is_should_add_neighbour(self, neighbours_list: List[int], new_neighbour_color: int) -> bool:
        """
        Нужно ли добавить neighbour в список соседей.
        """
        #List и count допустимо использовать, т.к. len(this_neighbour) относительно мал
        return not neighbours_list.count(new_neighbour_color)
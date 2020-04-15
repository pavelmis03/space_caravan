from typing import List

from constants.directions import side_di, side_dj
from map.level.rect.splitter import GridRectangle


class RectangleBypasserAbstract:
    """
    Класс для обхода по кругу сгенерированного прямоугольника из arr_after_split

    порядодк обхода:
    От верхней левой вправо. От нижней правой вверх. От нижней право влево. От верхней левой вниз
    """
    bypass_di = side_di[1], side_di[0], side_di[3], side_di[2]
    bypass_dj = [side_dj[1], side_dj[0], side_dj[3], side_dj[2]]
    def __init__(self, grid_rectangle: GridRectangle):
        """
        :param grid_rectangle: обрабатываемый прямоугольник
        """
        self._grid_rectangle = grid_rectangle

        self._start_pos = [grid_rectangle._left_top_index, grid_rectangle._bottom_right_index,
                           grid_rectangle._bottom_right_index, grid_rectangle._left_top_index]

    def _handle_cell(self, cycle: int, i: int, j: int,
                     arr: List[List[int]], grid) -> bool:
        """
        Обработка клетки (что мы должны делать на каждой итерации обхода)
        :return: True, если нужно продолжать обход. Иначе False
        """
        pass

    def _bypass(self, arr: List[List[int]], grid):
        """
        Обход self._grid_rectangle по кругу

        :param arr: список после разбиения сетки на прямоугольники
        :param grid: сетка
        """
        self._color = arr[self._grid_rectangle.top_index + 1][self._grid_rectangle.left_index + 1]

        for cycle in range(len(self.bypass_di)):
            i = self._start_pos[cycle][0]
            j = self._start_pos[cycle][1]
            while self._grid_rectangle.is_index_in_inside(i, j):
                should_break = not self._handle_cell(cycle, i, j, arr, grid)
                if should_break:
                    break
                i += self.bypass_di[cycle]
                j += self.bypass_dj[cycle]
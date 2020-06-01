from typing import List

from enemy_interaction_with_grid.vision.rectangle_bypass.rectangle_bypasser import RectangleBypasserAbstract


class ArrCorrecter(RectangleBypasserAbstract):
    """
    arr_after_slit содержит нули. Они обозначают стены. Для удобной работы их следует заменить на
    цвет ближайшей комнаты. Из-за того, что это делается для каждой комнаты, некоторые стены будут перекрашены
    несколько раз.
    """

    def _handle_cell(self, cycle: int, i: int, j: int,
                     arr: List[List[int]], grid) -> bool:
        """
        Присваивает клетке цвет.
        :return: True
        """
        arr[i][j] = self._color
        return True

    def correct_arr_after_split(self, arr: List[List[int]], grid):
        """
        Корректирует двумерный список.
        """
        super()._bypass(arr, grid)

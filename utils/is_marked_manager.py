"""
Модуль is_marked_manager.
Несколько классов для маркировки определенных ячеек
"""
from typing import List


class IsMarkedManagerAbstract:
    """
    Абстрактный класс isMarked.
    Нужен для маркировки данных по индексам и быстрым ответам на запрос о маркировке.
    """

    def __init__(self, arr: List[any]):
        """
        self._marked - список, в котором хранятся числа маркировки.
        Заполняется на основе arr.
        """
        self._mark_counter = 1
        self._marked = []
        self._fill_marked(arr)

    def _fill_marked(self, arr: List[any]):
        """
        заполнение self._marked
        """
        pass

    def next_iteration(self):
        """
        О(1) времени

        Следующая итерация - нужно забыть все старые значения и начать сначала.
        Чтобы лишний раз не проходиться по спискам и не обнулять ячейки,
        увеличиваем счетчик self._mark_counter. Ячейки должны считаться
        marked, если они равны self._mark_counter.
        """
        self._mark_counter += 1

    def _get_by_indexes(self, *indexes) -> any:
        """
        получить значение по indexes из self._marked
        """
        pass

    def _set_by_indexes(self, value: any, *indexes):
        """
        присвоить значение по indexes в self._marked
        """
        pass

    def mark(self, *indexes):
        """
        Отметить значение. Местонахождение определяется по indexes.
        Обычно 0(1) памяти
        """
        self._set_by_indexes(self._mark_counter, *indexes)

    def is_marked(self, *indexes) -> bool:
        """
        Ответить на запрос. Местонахождение определяется по indexes.
        Обычно 0(1) памяти
        """
        return self._get_by_indexes(*indexes) == self._mark_counter


class IsMarkedManager(IsMarkedManagerAbstract):
    """
    Отмечает клетки в одномерном массиве
    """

    def _fill_marked(self, arr: List[int]):
        """
        O(len(arr)) памяти и времени.
        """
        self._marked = [0 for i in range(len(arr))]

    def _get_by_indexes(self, *indexes):
        """
        в indexes только 1 индекс
        """
        i = indexes[0]
        return self._marked[i]

    def _set_by_indexes(self, value: int, *indexes):
        """
        в indexes только 1 индекс
        """
        i = indexes[0]
        self._marked[i] = value


class TwoDimensionalIsMarkedManager(IsMarkedManagerAbstract):
    """
    нужен для того, чтобы отмечать клетки в двумерном массиве.
    Используется в map.level.enemy_interaction_with_grid

    TwoDimensionalIsMarkedManager и IsMarkedManager похожи,
    но не знаю как избавиться от дублирования кода
    """

    def _fill_marked(self, arr: List[List[int]]):
        """
        O(len(arr)) памяти и времени.
        """
        self._marked = [[0] * len(arr[i]) for i in range(len(arr))]

    def _get_by_indexes(self, *indexes):
        """
        в indexes 2 индекса
        """
        i = indexes[0]
        j = indexes[1]
        return self._marked[i][j]

    def _set_by_indexes(self, value: int, *indexes):
        """
        в indexes 2 индекса
        """
        i = indexes[0]
        j = indexes[1]
        self._marked[i][j] = value

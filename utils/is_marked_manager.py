from typing import List


class IsMarkedManager:
    """
    нужен для того, чтобы отмечать клетки в двумерном массиве.
    Используется в map.level.interaction_with_enemy

    Специфика работы:
    работает быстро т.к. не проходится лишний раз по всему списку
    и не обнуляет значения.
    """
    def __init__(self, arr: List[List[int]]):
        """
        O(len(arr) * len(arr[0])) памяти и времени.
        """
        self._marked = [[0] * len(arr[0]) for i in range(len(arr))]
        self._mark_counter = 1

    def next_iteration(self):
        """
        O(1) времени
        """
        self._mark_counter += 1

    def mark(self, i: int, j: int):
        """
        O(1) времени
        """
        self._marked[i][j] = self._mark_counter

    def is_marked(self, i: int, j: int) -> bool:
        """
        O(1) времени
        """
        return (self._marked[i][j] == self._mark_counter)
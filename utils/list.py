"""
полезные функции для работы с двумерным массивом
"""
from typing import List


def is_indexes_correct(arr: List[List[any]], i: int, j: int) -> bool:
    """
    не выходят ли индексы за границы списка
    """
    return 0 <= i < len(arr) and 0 <= j < len(arr[i])

def get_list_without_equal_elements(arr: List[any]) -> List[any]:
    """
    :param arr: одномерный список. Не изменяется
    :return: отсортированный список без одинаковых элементов
    """
    sorted_arr = sorted(arr)
    result = []
    i = 0
    while i < len(sorted_arr):
        old = sorted_arr[i]
        while i < len(sorted_arr) and sorted_arr[i] == old:
            i += 1
        result.append(old)
    return result

def delete_element(arr: List[any], i: int):
    """
    Удаление элемента (O(1) асимптотика).
    Порядок в списке не сохраняется (На место i попадает последний эл-т, если i - не последний эл-т).
    :param arr: список
    :param i: индекс
    """
    arr[i], arr[-1] = arr[-1], arr[i]
    arr.pop()

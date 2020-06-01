from typing import List, Tuple
from random import randint
from random import random


def is_random_proc(chance: int = 50) -> bool:
    """
    min chance value = 0
    max chance value = 100
    """
    return randint(0, 99) < chance


def weight_choice(arr: List[Tuple[int, any]]) -> any:
    """
    Выбрать случайный элемент из списка arr. O(arr)

    :param l: Список[(вероятность, элемент)]. Сумма вероятностей должна быть равна 100
    :return: выбранный элемент
    """
    choice_int = randint(0, 99)

    chance = 0
    for item in arr:
        chance += item[0]
        if choice_int < chance:
            return item[1]

    raise Exception('sum of arr not equal 100')


def is_accurate_random_proc(chance: float) -> bool:
    """
    min chance value = 0
    max chance value = 100
    """
    return random() * 100.0 < chance


def shuffle(arr):
    for i in range(len(arr) - 1, 0, -1):
        j = randint(0, i)

        arr[i], arr[j] = arr[j], arr[i]

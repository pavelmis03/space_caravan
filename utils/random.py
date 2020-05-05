from random import randint
from random import random


def is_random_proc(chance: int = 50) -> bool:
    """
    min chance value = 0
    max chance value = 100
    """
    return randint(0, 99) < chance


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

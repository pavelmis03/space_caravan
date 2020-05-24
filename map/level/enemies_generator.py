from random import random
from typing import List

from drawable_objects.enemy import Enemy
from map.level.rect.splitter import GridRectangle
from utils.random import is_accurate_random_proc
from random import randint


def create_enemy(grid, i: int, j: int):
    """
    Создать врага под данным индексом с рандомным поворотом.
    """
    enemy = Enemy(grid.scene, grid.controller, grid.get_center_of_cell_by_indexes(i, j), random())
    grid.scene.enemies.append(enemy)

class EnemyGenerator:
    """
    Генератор Enemies.
    """
    def __init__(self, grid, rectangles: List[GridRectangle]):
        self.__grid = grid
        self.__rectangles = rectangles

    def generate(self):
        """
        Генерирует одного врага в какой-то клетке в каждой комнате с некоторой вероятностью (где комната -
        прямоугольник, полученный при первоначальном разбиении grid на прямоугольники в generator).
        """
        CHANCE_SPAWN = 25
        SAFE_ZONE_DISTANCE = 35
        WALLS_MIN_DISTANCE = 2 #нужно, чтобы враги не спавнились прямо у стены
        for item in self.__rectangles:
            """
            Наверно, временное решение
            Нужно для того, чтобы враг не спавнился рядом с игроком.
            """
            if item.bottom_index < SAFE_ZONE_DISTANCE and \
                item.right_index < SAFE_ZONE_DISTANCE:
                continue

            if not is_accurate_random_proc(CHANCE_SPAWN):
                continue

            random_i = randint(item.top_index + WALLS_MIN_DISTANCE, item.bottom_index - WALLS_MIN_DISTANCE)
            random_j = randint(item.left_index + WALLS_MIN_DISTANCE, item.right_index - WALLS_MIN_DISTANCE)
            if self.__grid.is_enemy_can_stay(random_i, random_j):
                # этот if вроде не нужен, но оставлю его, чтобы ничего не сломать (при будущих модификациях)
                create_enemy(self.__grid, random_i, random_j)
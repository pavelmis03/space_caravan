from typing import List, Tuple
from random import random, randint

from drawable_objects.enemy import Enemy
from drawable_objects.chest import Chest
from map.level.rect.splitter import GridRectangle
from utils.random import is_accurate_random_proc
from utils.random import weight_choice


def create_enemy(grid, i: int, j: int, weapon_name: str):
    """
    Создать врага под данным индексом с рандомным поворотом.
    """
    enemy = Enemy(grid.scene, grid.controller,
                  grid.get_center_of_cell_by_indexes(i, j), random())
    enemy.set_weapon(weapon_name)
    grid.scene.enemies.append(enemy)


def create_chest(grid, i: int, j: int, item_name: str):
    chest = Chest(grid.scene, grid.controller,
                    grid.get_center_of_cell_by_indexes(i, j), 0)
    chest.set_drop(item_name)
    grid.scene.game_objects.append(chest)


class LevelObjectsGenerator:
    """
    Генератор Enemies.
    """
    def __init__(self, grid, rectangles: List[GridRectangle],
                 enemy_weapons: List[Tuple[int, str]], chest_drop: List[Tuple[int, str]]):
        self.__grid = grid
        self.__rectangles = rectangles
        self.__enemy_weapons = enemy_weapons
        self.__chest_drop = chest_drop

    def generate(self):
        """
        Генерирует одного врага в какой-то клетке в каждой комнате с некоторой вероятностью (где комната -
        прямоугольник, полученный при первоначальном разбиении grid на прямоугольники в generator).
        """
        SAFE_ZONE_DISTANCE = 35
        for item in self.__rectangles:
            """
            Наверно, временное решение
            Нужно для того, чтобы враг не спавнился рядом с игроком.
            """
            if item.bottom_index < SAFE_ZONE_DISTANCE and \
                    item.right_index < SAFE_ZONE_DISTANCE:
                continue

            self.__generate_enemy(item)
            self.__generate_chest(item)

    def __generate_enemy(self, room: GridRectangle):
        CHANCE_SPAWN = 25

        if not is_accurate_random_proc(CHANCE_SPAWN):
            return

        random_i, random_j = self.__get_random_cell(room)

        if self.__grid.is_enemy_can_stay(random_i, random_j):
            # этот if вроде не нужен, но оставлю его, чтобы ничего не сломать (при будущих модификациях)
            random_weapon = weight_choice(self.__enemy_weapons)
            create_enemy(self.__grid, random_i, random_j, random_weapon)

    def __generate_chest(self, room: GridRectangle):
        CHANCE_SPAWN = 5

        if not is_accurate_random_proc(CHANCE_SPAWN):
            return
        random_i, random_j = self.__get_random_cell(room)

        random_item = weight_choice(self.__chest_drop)
        create_chest(self.__grid, random_i, random_j, random_item)

    def __get_random_cell(self, room: GridRectangle) -> Tuple[int, int]:
        WALLS_MIN_DISTANCE = 2  # нужно, чтобы объекты не спавнились прямо у стены

        random_i = randint(room.top_index + WALLS_MIN_DISTANCE,
                           room.bottom_index - WALLS_MIN_DISTANCE)
        random_j = randint(room.left_index + WALLS_MIN_DISTANCE,
                           room.right_index - WALLS_MIN_DISTANCE)

        return (random_i, random_j)

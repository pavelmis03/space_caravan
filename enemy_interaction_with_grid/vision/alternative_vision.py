from math import ceil
from typing import Tuple

from map.level.grid import LevelGrid as LevelGridClass
from enemy_interaction_with_grid.hearing.manager import EnemyHearingManager
from drawable_objects.enemy import Enemy
from geometry.rectangle import Rectangle
from utils.list import is_indexes_correct


class EnemyVisionWizard:
    VISION_RADIUS = Enemy.VISION_RADIUS



    def __init__(self, grid, hearing_manager: EnemyHearingManager):
        self.__grid = grid
        self.__hearing_manager = hearing_manager
        self.__scene = self.__grid.scene
        self.__enemies = self.__scene.enemies
        self.__player = self.__scene.player

        self.__index_range = int(ceil(EnemyVisionWizard.VISION_RADIUS / self.__grid.cell_width))
        self.__cell_used = [[] for _ in range(2 * self.__index_range + 1)]
        for i in range(2 * self.__index_range + 1):
            self.__cell_used[i] = [False for _ in range(2 * self.__index_range + 1)]

    def __unite_rects(self, rect1: Rectangle, rect2: Rectangle) -> Rectangle:
        result_left = min(rect1.left, rect2.left)
        result_right = max(rect1.right, rect2.right)
        result_top = min(rect1.top, rect2.top)
        result_bottom = max(rect1.bottom, rect2.bottom)
        return Rectangle(result_left, result_top, result_right, result_bottom)

    def __get_cell_used(self, i: int, j: int) -> bool:
        if not is_indexes_correct(self.__cell_used, i + self.__index_range, j + self.__index_range):
            return True
        return self.__cell_used[i + self.__index_range][j + self.__index_range]

    def __set_cell_used(self, i: int, j: int, new_value: bool):
        self.__cell_used[i + self.__index_range][j + self.__index_range] = new_value

    def __get_wall_rect(self, i: int, j: int, player_index: Tuple[int, int]) -> Rectangle:
        if self.__get_cell_used(i, j):
            return None
        self.__set_cell_used(i, j, True)
        absolute_i = player_index[0] + i
        absolute_j = player_index[1] + j
        if not is_indexes_correct(self.__grid.arr, absolute_i, absolute_j):
            return None
        if self.__grid.is_passable(absolute_i, absolute_j):
            return None
        return self.__grid.get_collision_rect(absolute_i, absolute_j)

    def __make_long_rect(self, i: int, j: int, dir: Tuple[int, int], player_index: Tuple[int, int]) -> Rectangle:
        result_rect = self.__get_wall_rect(i, j, player_index)
        if not result_rect:
            return None
        while True:
            i += dir[0]
            j += dir[1]
            next_rect = self.__get_wall_rect(i, j, player_index)
            if not next_rect:
                break
            result_rect = self.__unite_rects(result_rect, next_rect)
        return result_rect


    def __get_united_rects(self):
        walls_rects = []
        player_index = self.__grid.get_index_by_pos(self.__player.pos)
        for i in range(-self.__index_range, self.__index_range + 1):
            for j in range(-self.__index_range, self.__index_range + 1):
                self.__set_cell_used(i, j, False)

        for i in range(-self.__index_range, self.__index_range + 1):
            for j in range(-self.__index_range, self.__index_range + 1):
                wall_rect = self.__get_wall_rect(i, j, player_index)
                if not wall_rect:
                    continue
                long_rect = self.__make_long_rect(i, j + 1, [0, 1], player_index)
                if not long_rect:
                    long_rect = self.__make_long_rect(i + 1, j, [1, 0], player_index)
                if long_rect:
                    wall_rect = self.__unite_rects(wall_rect, long_rect)
                walls_rects.append(wall_rect)

        return walls_rects

    def process_logic(self):
        walls_rects = self.__get_united_rects()

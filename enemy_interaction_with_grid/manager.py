from typing import List

from drawable_objects.enemy import Enemy
from enemy_interaction_with_grid.hearing.hearing_manager import EnemyHearingManager
from enemy_interaction_with_grid.vision.vision_manager import EnemyVisionManager
from geometry.point import Point
from map.level.rect.splitter import GridRectangle


class GridInteractionWithEnemyManager:
    """
    Enemy обладает слухом и зрением.

    слух отвечает за поиск кратчайшего пути.
    зрение отвечает на запросы, видит ли enemy player'а
    """
    def __init__(self, rectangles: List[GridRectangle],
                arr_after_split: List[List[int]],
                grid):
        self._hearing_manager = EnemyHearingManager(grid)
        self._vision_manager = EnemyVisionManager(rectangles, arr_after_split, grid)

    def is_enemy_see_player(self, enemy: Enemy) -> bool:
        """
        Видит ли enemy player'а
        """
        return self._vision_manager.is_enemy_see_player(enemy)

    def get_pos_to_move(self, enemy: Enemy) -> Point:
        """
        Получить следующую точку для движения.
        """
        return self._hearing_manager.get_pos_to_move(enemy)

    def is_enemy_can_stay(self, i: int, j: int) -> bool:
        """
        Может ли enemy стоять в клетке с индексами i, j
        """
        return self._hearing_manager.can_stay(i, j)

    def process_logic(self):
        """
        логика менеджера
        """
        self._hearing_manager.process_logic()
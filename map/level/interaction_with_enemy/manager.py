from typing import List
from drawable_objects.enemy import Enemy
from geometry.point import Point
#from map.level.grid import LevelGrid
from map.level.rect.splitter import GridRectangle
from map.level.interaction_with_enemy.hearing.hearing_manager import EnemyHearingManager
from map.level.interaction_with_enemy.vision.vision_manager import EnemyVisionManager

class InteractionWithEnemyManager:
    """
    Enemy обладает слухом и зрением.

    слух отвечает за поиск кратчайшего пути.
    зрение отвечает на запросы, видит ли enemy player'а
    """
    def __init__(self, rectangles: List[GridRectangle],
                arr_after_split: List[List[int]],
                grid):
        self.hearing_manager = EnemyHearingManager(grid)
        self.vision_manager = EnemyVisionManager(rectangles, arr_after_split, grid)

    def is_enemy_see_player(self, enemy: Enemy) -> bool:
        return self.vision_manager.is_enemy_see_player(enemy)

    def get_pos_to_move(self, enemy: Enemy) -> Point:
        return self.hearing_manager.get_pos_to_move(enemy)

    def can_stay(self, i: int, j: int):
        return self.hearing_manager.can_stay(i, j)

    def process_logic(self):
        self.hearing_manager.process_logic()
        self.vision_manager.process_logic()
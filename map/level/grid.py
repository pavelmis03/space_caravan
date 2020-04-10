from typing import List
from map.collision_grid.collision_grid import CollisionGrid
from map.level.generator import LevelGenerator
from controller.controller import Controller
from drawable_objects.base import GameSprite
from drawable_objects.enemy import Enemy
from geometry.point import Point
from geometry.rectangle import Rectangle, create_rectangle_with_left_top
from geometry.segment import Segment
from map.grid import Grid
from map.level.generator import LevelGenerator, EnemyGenerator
from map.collision_grid.grid_interaction_with_enemy.manager import GridInteractionWithEnemyManager
from map.collision_grid.draw_static_manager import GridDrawStaticManager
from scenes.base import Scene
from map.collision_grid.intersection_manager import GridIntersectionManager

class LevelGrid(CollisionGrid):
    """
    Сетка уровня (данжа).
    """
    def enemy_generation(self):
        """
        Генерация врагов с помощью EnemyGenerator
        """
        enemy_generator = EnemyGenerator(self)
        enemy_generator.generate()

    def map_construction(self, min_area: int = 100, min_w: int = 8, min_h: int = 8):
        """
        Генерация уровня с помощью LevelGenerator
        """
        generator = LevelGenerator(self.arr, min_area, min_w, min_h)
        generator.generate()

    def process_logic(self):
        self.enemy_interaction_manager.process_logic()

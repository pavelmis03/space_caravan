from typing import List
from map.collision_grid import CollisionGrid
from map.level.generator import LevelGenerator
from drawable_objects.base import GameSprite
from geometry.point import Point
from geometry.rectangle import Rectangle, create_rect_with_center
from controller.controller import Controller
from scenes.base import Scene
from map.level.grid_static_draw_manager import GridStaticDrawManager

class LevelGrid(CollisionGrid):
    """
    Сетка уровня (данжа).
    """
    def map_construction(self, min_area: int = 100, min_w: int = 8, min_h: int = 8):
        """
        Генерация лабиринта с помощью LevelGenerator.
        """
        generator = LevelGenerator(self.arr, min_area, min_w, min_h)
        generator.generate()

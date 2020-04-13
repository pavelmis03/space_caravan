from map.collision_grid.collision_grid import CollisionGrid
from geometry.point import Point
from map.level.generator import LevelGenerator, EnemyGenerator

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

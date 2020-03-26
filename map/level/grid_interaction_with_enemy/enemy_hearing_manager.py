from map.level.grid_path_finder import GridPathFinder
from drawable_objects.enemy import Enemy

class EnemyHearingManager:
    """
    Не доделано
    """
    def __init__(self, grid_path_finder: GridPathFinder):
        self.grid_path_finder = grid_path_finder

    def add_enemy(self, enemy: Enemy):
        self.grid_path_finder.add_enemy(enemy)

    def process_logic(self):
        self.grid_path_finder.find_path_to_enemies(Enemy.HEARING_RANGE)
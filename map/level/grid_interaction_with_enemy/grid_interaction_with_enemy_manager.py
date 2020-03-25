from drawable_objects.enemy import Enemy
from map.level.grid_interaction_with_enemy.enemy_vision_manager import EnemyVisionManager
from map.level.grid_interaction_with_enemy.enemy_hearing_manager import EnemyHearingManager
from map.level.grid_path_finder import GridPathFinder

class GridInteractionWithEnemyManager:
    """
    Возможны ошибки:
    если два enemy в одной клетке
    если enemy в клетке с player
    """
    def __init__(self, grid):
        self.grid_path_finder = GridPathFinder(grid)
        self.enemy_vision_manager = EnemyVisionManager(self.grid_path_finder)
        self.enemy_hearing_manager = EnemyHearingManager(self.grid_path_finder)

    def set_enemy_in_arr(self, enemy: Enemy):
        self.enemy_hearing_manager.add_enemy(enemy)
        self.enemy_vision_manager.add_enemy(enemy)

    def process_logic(self):
        self.enemy_vision_manager.process_logic()
        self.enemy_hearing_manager.process_logic()
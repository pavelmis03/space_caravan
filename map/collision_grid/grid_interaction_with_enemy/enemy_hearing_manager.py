from drawable_objects.enemy import Enemy
from geometry.point import Point
from map.collision_grid.grid_interaction_with_enemy.path_finder import GridPathFinder


class EnemyHearingManager:
    """
    Не доделано до конца.
    Enemy должен реагировать на выстрел игрока
    """
    def __init__(self, grid):
        self.grid_path_finder = GridPathFinder(grid)

    def get_pos_to_move(self, enemy: Enemy) -> Point:
        return self.grid_path_finder.get_pos_to_move(enemy)

    def can_stay(self, i: int, j: int):
        return self.grid_path_finder.can_stay[i][j]

    def process_logic(self):
        self.grid_path_finder.find_path_to_enemies(Enemy.HEARING_RANGE)
from drawable_objects.enemy import Enemy
from geometry.point import Point
from map.level.interaction_with_enemy.hearing.path_finder import GridPathFinder


class EnemyHearingManager:
    """
    Сейчас представляет собой обертку для path_finder

    Не доделано до конца.
    Enemy должен реагировать на выстрел игрока (или нет)
    """
    def __init__(self, grid):
        self.path_finder = GridPathFinder(grid)

    def get_pos_to_move(self, enemy: Enemy) -> Point:
        return self.path_finder.get_pos_to_move(enemy)

    def can_stay(self, i: int, j: int):
        return self.path_finder.can_stay[i][j]

    def process_logic(self):
        self.path_finder.update_path_to_enemies(Enemy.HEARING_RANGE)
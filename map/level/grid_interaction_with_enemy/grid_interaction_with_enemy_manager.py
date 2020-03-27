from drawable_objects.enemy import Enemy
from geometry.segment import Segment
from map.level.grid_interaction_with_enemy.enemy_hearing_manager import EnemyHearingManager
from geometry.point import Point

class GridInteractionWithEnemyManager:
    def __init__(self, grid):
        self.grid = grid
        self.enemy_hearing_manager = EnemyHearingManager(grid)

    def is_enemy_see_player(self, enemy: Enemy) -> bool:
        player_pos = self.grid.scene.player.pos
        segment = Segment(enemy.pos, player_pos)
        if segment.length > Enemy.VISION_RADIUS:
            return False

        intersect_point = self.grid.intersect_seg_walls(segment)
        return (intersect_point is None)

    def get_pos_to_move(self, enemy: Enemy) -> Point:
        return self.enemy_hearing_manager.get_pos_to_move(enemy)

    def can_stay(self, i: int, j: int):
        return self.enemy_hearing_manager.can_stay(i, j)

    def process_logic(self):
        self.enemy_hearing_manager.process_logic()
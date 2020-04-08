from typing import List
from drawable_objects.enemy import Enemy
#from map.level.interaction_with_enemy.vision.vision_walls_intersection import VisionWallsIntersection
from map.level.interaction_with_enemy.vision.collision_rect_graph import RoomsGraph
from geometry.segment import Segment
from map.level.rect.splitter import GridRectangle


class EnemyVisionManager:
    """
    Vision распространяется только по сторонам квадрата.

    Обертка для VisionWallsIntersection

    Enemy видит Player если
    прямая, соединяющая клетку Player и клетку данного Enemy не
    пересекает стены (в действительности алгоритм неточен и
    работает немного по-другому, зато быстро. см. VisionWallsIntersection)
    """
    def __init__(self, rectangles: List[GridRectangle],
                arr_after_split: List[List[int]],
                grid):
        self.vision_walls_intersection = RoomsGraph(rectangles, arr_after_split, grid)
        self._grid = grid

    def is_enemy_see_player(self, enemy: Enemy) -> bool:
        """
        Может быть, нужно еще учитывать поворот Enemy.
        """
        enemy_pos = enemy.pos
        player_pos = self._grid.scene.player.pos

        segment = Segment(enemy_pos, player_pos) #важен порядок точек

        if segment.length >= Enemy.VISION_RADIUS:
            return False

        return not self.vision_walls_intersection.is_seg_intersect_wall(segment)

    def process_logic(self):
        pass
        #self.vision_walls_intersection.update_cant_see_to_enemies(Enemy.VISION_RANGE)
from typing import List

from drawable_objects.enemy import Enemy
from enemy_interaction_with_grid.vision.room.graph import RoomsGraph
from geometry.segment import Segment
from map.level.rect.splitter import GridRectangle


class EnemyVisionManager:
    """
    Отвечает за vision Enemy

    Обертка для RoomsGraph

    Enemy видит Player если, Enemy в радиусе видимости и прямая, соединяющая клетку Player и клетку данного Enemy не
    пересекает стены.
    Может быть, нужно еще учитывать поворот Enemy.
    """
    def __init__(self, rectangles: List[GridRectangle],
                arr_after_split: List[List[int]],
                grid):
        self.rooms_graph = RoomsGraph(rectangles, arr_after_split, grid)
        self._grid = grid

    def is_enemy_see_player(self, enemy: Enemy) -> bool:
        """
        Видит ли enemy player'а
        """
        segment = Segment(enemy.pos, self._grid.scene.player.pos) #важен порядок точек

        if segment.length >= Enemy.VISION_RADIUS:
            return False

        return not self.rooms_graph.is_seg_intersect_wall(segment)
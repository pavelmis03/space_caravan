from typing import List

from drawable_objects.enemy import Enemy
from enemy_interaction_with_grid.vision.room.graph import RoomsGraph
from geometry.optimized.segment import StaticSegment
from map.level.rect.splitter import GridRectangle
from geometry.sector import Sector
from math import pi


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

    def is_enemy_see_player(self, enemy, radius: float) -> bool:
        """
        Видит ли enemy player'а

        :param enemy: враг
        :param radius: радиус, в котором player должен находиться
        :return: bool
        """
        segment = StaticSegment(
            enemy.pos, self._grid.scene.player.pos)  # важен порядок точек

        if not self.__is_player_in_vision_sector(enemy, radius):
            return False

        return not self.rooms_graph.is_seg_intersect_wall(segment)

    def __is_player_in_vision_sector(self, enemy: Enemy, radius: float) -> bool:
        """
        Находится ли Player в секторе обзора enemy
        """
        sector = Sector(radius, enemy.pos, enemy.angle, enemy.VIEW_ANGLE)
        return sector.is_inside(self._grid.scene.player.pos)

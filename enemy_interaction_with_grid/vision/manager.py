from typing import List

from drawable_objects.enemy import Enemy
from enemy_interaction_with_grid.vision.room.graph import RoomsGraph
from geometry.optimized.segment import StaticSegment
from map.level.rect.splitter import GridRectangle
from math import pi
from geometry.triangle import is_point_in_triangle
from geometry.vector import vector_from_length_angle


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
        segment = StaticSegment(enemy.pos, self._grid.scene.player.pos) #важен порядок точек

        if not self.__is_player_in_vision_triangle(enemy):
            return False

        return not self.rooms_graph.is_seg_intersect_wall(segment)

    def __is_player_in_vision_triangle(self, enemy: Enemy) -> bool:
        """
        Находится ли Player в треугольнике обзора enemy

        Треугольник обзора - равнобедренный треугольник с вершиной в enemy.pos, боковыми сторонами Enemy.VISION_RADIUS
        и с углом между боковыми сторонами Enemy.VISION_ANGLE.
        """
        side_length = Enemy.VISION_RADIUS
        half_vision_angle = Enemy.VISION_ANGLE / 2

        direction_vector1 = vector_from_length_angle(side_length, enemy.angle + half_vision_angle)
        direction_vector2 = vector_from_length_angle(side_length, enemy.angle - half_vision_angle)

        return is_point_in_triangle(self._grid.scene.player.pos, enemy.pos, enemy.pos + direction_vector1,
                                                                            enemy.pos + direction_vector2)
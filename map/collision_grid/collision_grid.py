from typing import List, Dict

from drawable_objects.base import GameSprite
from geometry.point import Point
from geometry.rectangle import Rectangle, create_rectangle_with_left_top
from geometry.segment import Segment
from map.collision_grid.draw_static_manager import GridDrawStaticManager
from map.collision_grid.intersection_manager import GridIntersectionManager
from map.grid import Grid
from constants.grid import CELL_SIZE


class CollisionGrid(Grid):
    """
    Игровая сетка.
    Представляет собой двумерный список объектов,
    либо стена, либо пол.
    Все они статические (не меняются со временем).

    Генерируется в map_construction, далее преобразует
    инты в объекты.
    """
    FILENAMES = ['level.wall1', 'level.floor3']

    def initialize(self):
        self._fill_arr(CELL_SIZE, CELL_SIZE)

    def _fill_arr(self, cell_width: int, cell_height: int,
                 width_arr: int = 100, height_arr: int = 100):
        super()._fill_arr(0, cell_width, cell_height, width_arr, height_arr)
        self.map_construction()

        self.transform_ints_to_objects()

        self._other_initialize()

        self.enemy_generation()

    def _other_initialize(self):
        self.static_draw_manager = GridDrawStaticManager(self)
        self.grid_intersection_manager = GridIntersectionManager(self)

    def enemy_generation(self):
        """
        Спавн врагов на уровне
        """
        pass

    def map_construction(self):
        """
        Построение уровня (стен и пола)
        """
        pass

    def process_draw(self):
        self.static_draw_manager.process_draw()

    def transform_ints_to_objects(self):
        """
        Необходимо применять после генерации.
        """
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                pos_x = self.pos.x + j * self.cell_width + self.cell_width / 2
                pos_y = self.pos.y + i * self.cell_height + self.cell_height / 2
                filename_index = int(bool(self.arr[i][j]))

                self.arr[i][j] = GameSprite(self.scene, self.controller,
                                            CollisionGrid.FILENAMES[filename_index], Point(pos_x, pos_y))

    def is_passable(self, i: int, j: int) -> bool:
        return self.arr[i][j].image_name != CollisionGrid.FILENAMES[0]

    def get_collision_rect(self, i: int, j: int) -> Rectangle:
        h = self.cell_height
        w = self.cell_width
        y = i * h
        x = j * w
        return create_rectangle_with_left_top(Point(x, y) + self.pos, w, h)

    def get_collision_rects_nearby(self, pos: Point) -> List[Rectangle]:
        """
        Возвращает все прямоугольники коллизий статических объектов (стен)
        в квадрате длиной (1 + INDEX_OFFSET * 2) с центром в клетке,
        соответствующей координате pos.
        :param pos:
        :return:
        """
        center_i, center_j = self.index_manager.get_index_by_pos(pos)
        INDEX_OFFSET = 2

        min_i = max(0, center_i - INDEX_OFFSET)
        min_j = max(0, center_j - INDEX_OFFSET)
        max_i = min(len(self.arr), center_i + INDEX_OFFSET + 1)
        max_j = min(len(self.arr[0]), center_j + INDEX_OFFSET + 1)

        res = []
        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                if not self.is_passable(i, j):
                    res.append(self.get_collision_rect(i, j))
        return res

    def intersect_seg_walls(self, seg: Segment) -> Point:
        return self.grid_intersection_manager.intersect_seg_walls(seg)

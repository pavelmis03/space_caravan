from typing import List
from map.grid import Grid
from map.level.generator import LevelGenerator
from drawable_objects.base import GameSprite
from drawable_objects.enemy import Enemy
from geometry.point import Point
from geometry.rectangle import Rectangle, create_rect_with_center
from controller.controller import Controller
from scenes.base import Scene
from map.level.grid_static_draw_manager import GridStaticDrawManager
from map.level.grid_path_manager import GridPathManager

class LevelGrid(Grid):
    """
    Сетка уровня (данжа).
    Представляет собой двумерный список объектов,
    либо стена, либо пол.
    Все они статические (не меняются со временем).

    Генерируется с помощью LevelGenerator, далее преобразует
    инты в объекты.
    """
    def __init__(self, scene: Scene, controller: Controller, pos: Point,
                 cell_width: int, cell_height: int,
                 width: int = 100, height: int = 100,
                 min_area: int = 100, min_w: int = 8, min_h: int = 8):
        super().__init__(scene, controller, pos, 0, cell_width, cell_height, width, height)

        generator = LevelGenerator(self.arr, min_area, min_w, min_h)
        generator.generate()

        self.transform_ints_to_objects()
        self.static_draw_manager = GridStaticDrawManager(self)
        self.path_manager = GridPathManager(self)

    def process_draw(self):
        self.static_draw_manager.process_draw()

    def process_logic(self):
        self.path_manager.path_finding()

    def transform_ints_to_objects(self):
        """
        Необходимо применять после генерации.
        """
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                pos_x = self.pos.x + j * self.cell_width
                pos_y = self.pos.y + i * self.cell_height
                filenames = ['wall', 'floor']
                filename_index = int(bool(self.arr[i][j]))

                self.arr[i][j] = GameSprite(self.scene, self.controller,
                           filenames[filename_index], Point(pos_x, pos_y))

    def is_passable(self, i: int, j: int) -> bool:
        return self.arr[i][j].image_name != 'wall'

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
                    h = self.cell_height
                    w = self.cell_width
                    y = i * h
                    x = j * w
                    res.append(create_rect_with_center(Point(x, y), w, h))
        return res

    def set_enemy_in_arr(self, enemy: Enemy):
        self.path_manager.set_enemy_in_arr(enemy)

from typing import List

from map.grid import Grid
from map.level.generator import LevelGenerator

from drawable_objects.base import GameSprite
from geometry.point import Point
from geometry.rectangle import Rectangle, create_rect_with_center

from controller.controller import Controller
from scenes.base import Scene

from drawable_objects.background.transfusion_background import TransfusionBackground, RGB
from drawable_objects.background.gradient_background import GradientBackground, RGB

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
        """
        :param scene:
        :param controller:
        :param cell_width:
        :param cell_height:
        :param width:
        :param height:
        :param min_area:
        :param min_w:
        :param min_h:
        """
        super().__init__(scene, controller, pos, 0, cell_width, cell_height, width, height)

        generator = LevelGenerator(self.arr, min_area, min_w, min_h)
        generator.generate()

        self.transform_ints_to_objects()

        #self.background = TransfusionBackground(scene, controller, pos,
        #        (RGB(64, 0, 0), RGB(0, 64, 0), RGB(0, 0, 64)))

        self.background = GradientBackground(scene, controller, 'dungeon_background', pos,
                                             RGB(19, 135, 8), RGB(0, 0, 0))
        #RGB(19, 135, 8), RGB(0, 0, 0))
    def process_draw(self):
        self.background.process_draw()
        super().process_draw()

    def process_logic(self):
        self.background.process_logic()
        pass

    def transform_ints_to_objects(self):
        """
        Необходимо применять после генерации.
        :return:
        """
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                pos_x = self.pos.x + j * self.cell_width
                pos_y = self.pos.y + i * self.cell_height
                filenames = ['wall', 'floor']
                filename_index = int(bool(self.arr[i][j]))

                self.arr[i][j] = GameSprite(self.scene, self.controller,
                           filenames[filename_index], Point(pos_x, pos_y))

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
                if self.arr[i][j].image_name == 'wall':
                    """
                    простая проверка, но в выдумывании чего-то другого
                    нет необходимости.
                    """
                    h = self.cell_height
                    w = self.cell_width
                    y = i * h
                    x = j * w
                    res.append(create_rect_with_center(Point(x, y), w, h))
        return res
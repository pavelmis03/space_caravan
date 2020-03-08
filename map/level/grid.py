from map.grid import Grid
from map.level.generator import Generator

from drawable_objects.player import GameSprite
from geometry.point import Point

from controller.controller import Controller
from scenes.base import Scene

class LevelGrid(Grid):
    def __init__(self, scene: Scene, controller: Controller, pos: Point,
                 cell_width: int, cell_height: int,
                 width: int = 500, height: int = 500,
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

        generator = Generator(self.arr, min_area, min_w, min_h)
        generator.generate()

        self.transform_ints_to_objects()

    def transform_ints_to_objects(self):
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                pos_x = self.pos.x + j * self.cell_width
                pos_y = self.pos.y + i * self.cell_height
                filenames = ['images/floor.png', 'images/wall.png']
                filename_index = int(bool(self.arr[i][j]))

                self.arr[i][j] = GameSprite(self.scene, self.controller,
                           filenames[filename_index], Point(pos_x, pos_y))
from typing import Dict, Tuple

from drawable_objects.base import DrawableObject

from geometry.point import Point

from controller.controller import Controller
from scenes.base import Scene

class Grid(DrawableObject):
    def __init__(self, scene: Scene, controller: Controller, pos: Point,
                 default_value: any,
                 cell_width: int, cell_height: int,
                 width: int=100, height: int=100):
        """

        :param scene:
        :param controller:
        :param width:
        :param height:
        :param default_value:
        """
        super().__init__(scene, controller, pos)

        self.cell_width = cell_width
        self.cell_height = cell_height

        self.width = width
        self.height = height
        self.arr = [[default_value] * self.width for i in range(self.height)]

    def process_draw(self, relative_center: Point):
        """
        Отрисовывает только объекты на экране

        :param relative_center:
        :return:
        """
        index_i, index_j = self.get_index_of_objects_on_screen(relative_center)

        for i in range(index_i['min'], index_i['max']):
            for j in range(index_j['min'], index_j['max']):
                self.arr[i][j].process_draw(relative_center)

    def get_index_of_objects_on_screen(self, relative_center: Point) \
            -> Tuple[Dict[str, int], Dict[str, int]]:

        offset_y = int(relative_center.y - self.pos.y)
        offset_x = int(relative_center.x - self.pos.x)

        i = {'min': offset_y // self.cell_height,
             'max': (self.scene.game.height + offset_y) // self.cell_height + 1}

        j = {'min': offset_x // self.cell_width,
             'max': (self.scene.game.width + offset_x) // self.cell_width + 1}

        i['min'] = max(i['min'], 0)
        i['max'] = min(i['max'], len(self.arr))

        j['min'] = max(j['min'], 0)
        j['max'] = min(j['max'], len(self.arr[0]))

        return i, j

    def process_logic(self):
        pass

    def print_arr(self):
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                print(self.arr[i][j], end='')
            print()
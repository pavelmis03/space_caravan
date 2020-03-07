from drawable_objects.base import DrawableObject

from geometry.point import Point

from controller.controller import Controller
from scenes.base import Scene

class Grid(DrawableObject):
    def __init__(self, scene: Scene, controller: Controller, pos: Point,
                 width: int=100, height: int=100, default_value=0):
        """

        :param scene:
        :param controller:
        :param width:
        :param height:
        :param default_value:
        """
        super().__init__(scene, controller, pos)

        self.width = width
        self.height = height
        self.arr = [[default_value] * self.width for i in range(self.height)]

    def process_draw(self, relative_center: Point):
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                self.arr[i][j].process_draw(relative_center)

    def process_logic(self):
        pass

    def print_arr(self):
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                print(self.arr[i][j], end='')
            print()
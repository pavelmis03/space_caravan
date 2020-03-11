from drawable_objects.base import DrawableObject

from geometry.point import Point

from controller.controller import Controller
from scenes.base import Scene

from map.gridCoordManager import GridCoordManager

class Grid(DrawableObject):
    """
    Прямоугольная сетка.
    """
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

        self.arr = [[default_value] * width for i in range(height)]

        self.coord_manager = GridCoordManager(self, self.pos, cell_width, cell_height)

    def process_draw(self):
        """
        Отрисовывает только объекты на экране

        :return:
        """
        relative_center = self.scene.relative_center
        index_i, index_j = self.coord_manager.get_coord_of_objects_on_screen(relative_center)

        for i in range(index_i['min'], index_i['max']):
            for j in range(index_j['min'], index_j['max']):
                self.arr[i][j].process_draw()

    def process_logic(self):
        pass

    def print_arr(self):
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                print(self.arr[i][j], end='')
            print()

    @property
    def cell_width(self):
        return self.coord_manager.cell_width
    @property
    def cell_height(self):
        return self.coord_manager.cell_height
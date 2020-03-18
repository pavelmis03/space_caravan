
from drawable_objects.base import DrawableObject

from geometry.point import Point

from controller.controller import Controller
from scenes.base import Scene

from map.gridIndexManager import GridIndexManager

class Grid(DrawableObject):
    """
    Прямоугольная сетка.
    """
    def __init__(self, scene: Scene, controller: Controller, pos: Point,
                 default_value: any,
                 cell_width: int, cell_height: int,
                 width: int=100, height: int=100):
        super().__init__(scene, controller, pos)

        self.arr = [[default_value] * width for i in range(height)]
        """
        расчет индексов по позиции делегирован index_manager
        """
        self.index_manager = GridIndexManager(self, self.pos, cell_width, cell_height)

    def process_draw(self):
        """
        Отрисовывает только объекты на экране
        """
        relative_center = self.scene.relative_center
        index_i, index_j = self.index_manager.get_corrected_indexes(
            self.index_manager.get_index_of_objects_on_screen(relative_center))

        for i in range(index_i['min'], index_i['max']):
            for j in range(index_j['min'], index_j['max']):
                self.arr[i][j].process_draw()

    def process_logic(self):
        """
        у статических объектов нет process_logic
        """
        pass

    def get_correct_relative_pos(self, relative_pos: Point) -> Point:
        """
        Принимает relative_pos, который должен быть.
        Далее возвращает такой relative_pos, чтобы то, что за пределами
        grid, не было видно.
        То есть, если игрок у левой границы, то камера
        смещается вправо.
        """
        i, j = self.index_manager.get_index_of_objects_on_screen(relative_pos)
        res_pos = Point(relative_pos.x, relative_pos.y)

        res_pos.x = max(res_pos.x, self.pos.x)
        res_pos.y = max(res_pos.y, self.pos.y)

        res_pos.x = min(res_pos.x, self.pos.x + self.width - self.scene.width)
        res_pos.y = min(res_pos.y, self.pos.y + self.height - self.scene.height)

        return res_pos

    @property
    def width(self):
        return self.cell_width * (len(self.arr[0]) - 1)

    @property
    def height(self):
        return self.cell_height * (len(self.arr) - 1)

    @property
    def cell_width(self):
        return self.index_manager.cell_width

    @property
    def cell_height(self):
        return self.index_manager.cell_height

    def print_arr(self):
        """
        для отладки
        """
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                print(self.arr[i][j], end='')
            print()
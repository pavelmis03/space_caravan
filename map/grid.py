from typing import Tuple, Dict

from drawable_objects.base import DrawableObject

from geometry.point import Point
from geometry.rectangle import create_rectangle_with_left_top

from controller.controller import Controller
from scenes.base import Scene

from map.grid_index_manager import GridIndexManager


class Grid(DrawableObject):
    """
    Прямоугольная сетка.
    """

    def __init__(self, scene: Scene, controller: Controller, pos: Point):
        super().__init__(scene, controller, pos)

    def _fill_arr(self, default_value: any,
                  cell_width: int, cell_height: int,
                  width_arr: int = 100, height_arr: int = 100):
        self.arr = [[default_value] * width_arr for i in range(height_arr)]
        self._arr_initialize(cell_width, cell_height)

    def _arr_initialize(self, cell_width: int, cell_height: int):
        """
        расчет индексов по позиции делегирован index_manager
        """
        self.index_manager = GridIndexManager(
            self, self.pos, cell_width, cell_height)

        width = cell_width * len(self.arr[0])
        height = cell_height * len(self.arr)
        self.grid_rectangle = create_rectangle_with_left_top(
            self.pos, width, height)

    def from_dict(self, data_dict: Dict):
        pass

    def to_dict(self):
        pass

    def process_draw(self):
        """
        Отрисовывает только объекты на экране
        """
        relative_center = self.scene.relative_center
        index_i, index_j = \
            self.index_manager.get_index_of_objects_on_screen(relative_center)

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
        res_pos = Point(relative_pos.x, relative_pos.y)

        res_pos.x = max(res_pos.x, self.left)
        res_pos.y = max(res_pos.y, self.top)

        res_pos.x = min(res_pos.x, self.right - self.scene.width)
        res_pos.y = min(res_pos.y, self.bottom - self.scene.height)

        return res_pos

    @property
    def width(self) -> float:
        return self.grid_rectangle.width

    @property
    def height(self) -> float:
        return self.grid_rectangle.height

    @property
    def left(self) -> float:
        return self.grid_rectangle.top_left.x

    @property
    def top(self) -> float:
        return self.grid_rectangle.top_left.y

    @property
    def right(self):
        return self.grid_rectangle.bottom_right.x

    @property
    def bottom(self):
        return self.grid_rectangle.bottom_right.y

    @property
    def cell_width(self):
        return self.index_manager.cell_width

    @property
    def cell_height(self):
        return self.index_manager.cell_height

    def get_center_of_cell_by_indexes(self, i: int, j: int) -> Point:
        return self.index_manager.get_center_of_cell_by_indexes(i, j)

    def get_index_by_pos(self, pos: Point) -> Tuple[int, int]:
        return self.index_manager.get_index_by_pos(pos)

    def print_arr(self):
        """
        для отладки
        """
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                print(self.arr[i][j], end='')
            print()

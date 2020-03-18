from typing import Dict, Tuple
from geometry.point import Point

class GridIndexManager:
    """
    Вынесена значитльная часть кода из Grid, чтобы класс был не слишком большим.
    Эта часть отвечает за обработку запросов, связанных с индексами, позицией grid
    """
    def __init__(self, grid, pos, cell_width, cell_height):
        self.grid = grid

        self.pos = pos
        self.cell_height = cell_height
        self.cell_width = cell_width

    def get_index_of_objects_on_screen(self, relative_center: Point) \
            -> Tuple[Dict[str, int], Dict[str, int]]:
        """
        Проходится по всем эл-там сетки затратно по времени, поэтому
        с помощью математики ищем интервалы координат, по которым следует пройтись

        Полученные индексы могут быть вне grid.arr, поэтому
        их нужно прогнать через метод get_corrected_indexes
        """

        pos = self.get_pos_in_grid_origin(relative_center)

        i_min, j_min = self.get_index_by_pos_in_grid_origin(pos)
        i = {'min': i_min,
             'max': (self.grid.scene.game.height + int(pos.y) + (self.cell_height - 1)) // self.cell_height + 1}

        j = {'min': j_min,
             'max': (self.grid.scene.game.width + int(pos.x) + (self.cell_width - 1)) // self.cell_width + 1}
        """
        Прибавляем (self.cell_height - 1) и (self.cell_width - 1) для деления с округлением вверх
        """
        i['min'] = i['min']
        i['max'] = i['max']

        j['min'] = j['min']
        j['max'] = j['max']

        return i, j

    def get_corrected_indexes(self, indexes: Tuple[Dict[str, int], Dict[str, int]]) -> \
            Tuple[Dict[str, int], Dict[str, int]]:
        i, j = indexes
        i['min'] = max(i['min'], 0)
        i['max'] = min(i['max'], len(self.grid.arr))

        j['min'] = max(j['min'], 0)
        j['max'] = min(j['max'], len(self.grid.arr[0]))

        return i, j

    def get_index_by_pos(self, pos: Point) -> Tuple[int, int]:
        relative_pos = self.get_pos_in_grid_origin(pos)
        return self.get_index_by_pos_in_grid_origin(relative_pos)

    def get_index_by_pos_in_grid_origin(self, pos: Point) -> Tuple[int, int]:
        """
        index эл-та на данной позиции в системе координат grid_origin
        """
        i = int(pos.y / self.cell_height)
        j = int(pos.x / self.cell_width)
        return i, j

    def get_pos_in_grid_origin(self, pos: Point) -> Point:
        """
        grid origin - система координат (математических) относительно grid.
        Обычно у grid позиция (0, 0), grid_origin поэтому совпадает
        с обычной системо координат.
        """
        return Point(pos.x - self.pos.x, pos.y - self.pos.y)
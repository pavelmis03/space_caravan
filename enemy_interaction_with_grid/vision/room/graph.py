from collections import deque
from typing import List

from enemy_interaction_with_grid.vision.rectangle_bypass.arr_correcter import ArrCorrecter

from geometry.point import Point
from geometry.segment import Segment
from enemy_interaction_with_grid.vision.room.room import Room
from map.level.rect.splitter import GridRectangle
from utils.is_marked_manager import IsMarkedManager


class RoomsGraph:
    """
    Граф комнат. Нужен для того, чтобы отвечать на запрос, пересекает ли отрезок какую-нибудь стену.
    """
    def __init__(self, rectangles: List[GridRectangle], arr_after_split: List[List[int]], grid):
        self._grid = grid
        self._arr_after_split = arr_after_split
        self._correct_arr_after_split(rectangles)

        self._used = IsMarkedManager(rectangles)
        self._rooms = self._get_all_rooms(rectangles)

    def is_seg_intersect_wall(self, seg: Segment) -> bool:
        """
        Пересекает ли Segment стены. Работает быстрее GridIntersectionManager для больших Segment (сопоставимых с
        размером комнат).

        Обход графа bfs'ом.
        :param seg: отрезок, который проверяем
        :return: bool
        """
        #часто встречается color - 1, т.к. arr_after_split содержит в себе цвета с 1, а индексация в списках с 0
        self._used.next_iteration()

        color0 = self._get_room_color_by_pos(seg.p1)
        self._used.mark(color0 - 1)

        queue = deque()
        queue.append(color0)

        while len(queue):
            color = queue.popleft()
            room = self._rooms[color - 1]

            if room.is_intersect(seg):
                return True

            neighbours = room.get_neighbours(seg)
            for i in range(len(neighbours)):
                neighbour_color = neighbours[i]
                if self._used.is_marked(neighbour_color - 1):
                    continue

                self._used.mark(neighbour_color - 1)
                queue.append(neighbour_color)

        return False

    def _get_room_color_by_pos(self, pos: Point) -> int:
        """
        получение цвета, в которую окрашена комната по позиции.
        """
        i0, j0 = self._grid.get_index_by_pos(pos)
        color = self._arr_after_split[i0][j0]
        return color

    def _get_all_rooms(self, grid_rectangles: List[GridRectangle]) -> List[Room]:
        """
        на основе grid_rectangles формирует все комнаты.
        """
        result = []
        for i in range(len(grid_rectangles)):
            new_room = Room(grid_rectangles[i], self._arr_after_split, self._grid)
            result.append(new_room)

        return result

    def _correct_arr_after_split(self, rectangles: List[GridRectangle]):
        """
        корректирует arr_after_split на основе всех rectangles
        """
        for i in range(len(rectangles)):
            correcter = ArrCorrecter(rectangles[i])
            correcter.correct_arr_after_split(self._arr_after_split, self._grid)

    def process_draw(self):
        """
        для debug

        отрисовывает внешние границы всех комнат одним из случайных цветов.
        """
        for i in range(len(self._rooms)):
            self._rooms[i].process_draw()
from typing import List, Tuple

from pygame import draw

from enemy_interaction_with_grid.vision.rectangle_bypass.collision_form_creator import CollisionFormCreator
from enemy_interaction_with_grid.vision.rectangle_bypass.rectangle_neighbours import RectangleNeighbours
from geometry.optimized.segment import StaticSegment
from geometry.rectangle import Rectangle
from geometry.optimized.rectangle import StaticRectangle
from geometry.optimized.intersections import is_segments_intersect, is_seg_rect_intersect
from map.level.rect.splitter import GridRectangle


class Room:
    """
    Комната. Имеет внешние границы (для перехода к соседним) и внутренние (для коллизий).
    """
    def __init__(self, grid_rectangle: GridRectangle,
                arr_after_split: List[List[int]],
                grid):
        self._grid = grid


        self._grid_rectangle = grid_rectangle

        self._outer_rectangle = self._get_outer_rectangle(grid)
        self._collision_rectangles = self._get_collision_rectangles(grid)
        self._neighbours = self._get_all_neighbours(arr_after_split, grid)

        self._drawer = RoomDrawer(self._grid, self._outer_rectangle, self._collision_rectangles)

    def is_intersect(self, seg: StaticSegment) -> bool:
        """
        Пересекает ли отрезок внутренние прямоугольники комнаты (то есть стены).
        """
        for i in range(len(self._collision_rectangles)):
            rect = self._collision_rectangles[i]
            if is_seg_rect_intersect(seg, rect):
                return True
        return False

    def get_neighbours(self, seg: StaticSegment) -> List[int]:
        """
        Получение соседних комнат, которых пересекат seg
        """
        edges = self._outer_rectangle.get_edges()
        result = []
        """
        порядок следования сторон совпадает с порядком следования
        neighbours, то есть по данному индексу стороне соответствует neighbour
        """
        for i in range(len(edges)):
            if is_segments_intersect(seg, edges[i]):
                result.extend(self._neighbours[i])

        return result

    def _get_all_neighbours(self, arr_after_split: List[List[int]], grid) -> \
                Tuple[List[int], List[int], List[int], List[int]]:
        """
        Создание и получение соседних комнат
        """
        group_of_neighour_rectangles = RectangleNeighbours(self._grid_rectangle)
        result = group_of_neighour_rectangles.get_neighbours(arr_after_split, grid)
        return result

    def _get_collision_rectangles(self, grid) -> List[StaticRectangle]:
        """
        Создание и получение прямоугольников коллизий
        """
        room_form = CollisionFormCreator(self._grid_rectangle)
        result = room_form.get_collision_rectangles(grid.arr, grid)
        return result

    def _get_outer_rectangle(self, grid) -> StaticRectangle:
        """
        Создание и получение прямоугольника внешних границ.
        """
        grid_rectangle = self._grid_rectangle
        left_top_cell = grid.get_collision_rect(grid_rectangle.top_index,
                                                grid_rectangle.left_index)

        right_bottom_cell = grid.get_collision_rect(grid_rectangle.bottom_index,
                                                    grid_rectangle.right_index)

        return StaticRectangle(left_top_cell.left, left_top_cell.top,
            right_bottom_cell.right, right_bottom_cell.bottom)

    def process_draw(self):
        """
        Отрисовка для debug.
        """
        self._drawer.process_draw()


class RoomDrawer:
    """
    Отрисовка внутрених и внешних границ комнаты. (Для debug).
    """
    def __init__(self, grid, outer_rectangle: Rectangle, collision_rectangles: List[Rectangle]):
        self._grid = grid
        self._outer_rectangle = outer_rectangle
        self._collision_rectangles = collision_rectangles

    def _draw_rect(self, COLOR: Tuple[int, int, int], LINE_WIDTH: int,
                   rectangle: Rectangle):
        """
        Отрисовка прямоугольника.
        """
        dx = self._grid.scene.relative_center.x
        dy = self._grid.scene.relative_center.y

        draw.rect(self._grid.scene.screen, COLOR,
            (rectangle.left - dx, rectangle.top - dy, rectangle.width, rectangle.height), LINE_WIDTH)

    def draw_outer_rectangle(self):
        """
        Отрисовка внешних границ.
        """
        COLOR = (0, 255, 0)
        LINE_WIDTH = 10

        self._draw_rect(COLOR, LINE_WIDTH, self._outer_rectangle)

    def draw_collision_rectangles(self):
        """
        Отрисовка внутренних границ
        """
        COLOR = (255, 255, 255)
        LINE_WIDTH = 5

        for i in range(len(self._collision_rectangles)):
            self._draw_rect(COLOR, LINE_WIDTH, self._collision_rectangles[i])

    def process_draw(self):
        """
        Отрисовка комнаты. Для debug.
        """
        self.draw_outer_rectangle()
        self.draw_collision_rectangles()
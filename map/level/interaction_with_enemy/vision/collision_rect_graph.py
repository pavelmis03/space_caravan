from utils.lists import is_indexes_correct
from typing import List, Tuple
from geometry.rectangle import Rectangle
from geometry.segment import Segment
from geometry.point import Point
from geometry.intersections import intersect_segments, intersect_seg_rect
from map.level.rect.splitter import GridRectangle
from constants.directions import side_di, side_dj
from utils.lists import get_list_without_equal_elements
from utils.is_marked_manager import IsMarkedManager
from collections import deque
from constants.directions import rect_di, rect_dj
from geometry.rectangle import rectangle_to_rect
from pygame import draw

class RectangleRoundBypasserAbstract:
    def __init__(self, grid_rectangle: GridRectangle):
        self.grid_rectangle = grid_rectangle

        self.start_pos = [grid_rectangle._left_top_index, grid_rectangle._bottom_right_index,
                          grid_rectangle._bottom_right_index, grid_rectangle._left_top_index]
        self.bypass_di = [side_di[1], side_di[0], side_di[3], side_di[2]]
        self.bypass_dj = [side_dj[1], side_dj[0], side_dj[3], side_dj[2]]

    def handle_cell(self, cycle: int, i: int, j: int,
                    arr: List[List[int]], grid) -> bool:
        """
        :return: True, если нужно продолжать обход. Иначе False
        """
        pass

    def bypass(self, arr: List[List[int]], grid):
        self._color = arr[self.grid_rectangle.top_index + 1][self.grid_rectangle.left_index + 1]

        for cycle in range(len(self.bypass_di)):
            i = self.start_pos[cycle][0]
            j = self.start_pos[cycle][1]
            while self.grid_rectangle.is_index_in_inside(i, j):
                should_break = not self.handle_cell(cycle, i, j, arr, grid)
                if should_break:
                    break
                i += self.bypass_di[cycle]
                j += self.bypass_dj[cycle]


class ArrAfterSplitCorrecter(RectangleRoundBypasserAbstract):
    def handle_cell(self, cycle: int, i: int, j: int,
                    arr: List[List[int]], grid) -> bool:
        arr[i][j] = self._color
        return True

    def correct_arr_after_split(self, arr: List[List[int]], grid):
        self.bypass(arr, grid)


class GroupOfRectangleNeighbours(RectangleRoundBypasserAbstract):
    neighbour_di = side_di
    neighbour_dj = side_dj
    def __init__(self, grid_rectangle: GridRectangle):
        super().__init__(grid_rectangle)
        self.top_neighbours = []
        self.right_neighbours = []
        self.bottom_neighbours = []
        self.left_neighbours = []

    def handle_cell(self, cycle: int, i: int, j: int,
                    arr: List[List[int]], grid) -> bool:
        neighbours = [self.top_neighbours, self.right_neighbours,
                      self.bottom_neighbours, self.left_neighbours]
        this_neighbour = neighbours[cycle]
        new_i = i + GroupOfRectangleNeighbours.neighbour_di[cycle]
        new_j = j + GroupOfRectangleNeighbours.neighbour_dj[cycle]
        if not is_indexes_correct(arr, new_i, new_j):
            """
            если индексы некорректные, то они уже не станут корректными
            в силу прямоугольности сетки
            """
            return False
        new_neighbour_color = arr[new_i][new_j]
        """
        List и count допустимо использовать, т.к.
        len(this_neighbour) относительно мал
        """
        if not this_neighbour.count(new_neighbour_color):
            this_neighbour.append(new_neighbour_color)

        return True

    def get_neighbours(self, arr: List[List[int]], grid) -> \
                Tuple[List[int], List[int], List[int], List[int]]:
        """
        Возвращает списки Rectangle, к которым можно перейти
        из данного. Порядок списков Rectangle: верхний, правый, нижний, левый.
        Причем возвращаются не копии, а оригинал. Но, думаю, с этим проблем не будет
        """
        self.bypass(arr, grid)
        return (self.top_neighbours, self.right_neighbours,
                self.bottom_neighbours, self.left_neighbours)

class RoomFigureFormCreator(RectangleRoundBypasserAbstract):
    def __init__(self, grid_rectangle: GridRectangle):
        super().__init__(grid_rectangle)
        self._collision_rectangles = []

        self.start_of_rect = None
        self.end_of_rect = None

        self.old_cycle = -1

    @property
    def is_rect_started(self) -> bool:
        return self.start_of_rect is not None

    def is_next_side(self, this_cycle: int) -> bool:
        return self.old_cycle != this_cycle

    def get_new_rectangle(self) -> Rectangle:
        """
        Нужно составить Rectangle, который является выпуклой оболочкой
        для всех вершин обоих прямоугольников. Самый простой способ -
        отсортировать все значения и взять граничные
        """
        vertices_x = [self.start_of_rect.left, self.start_of_rect.right,
                      self.end_of_rect.left, self.end_of_rect.right]
        vertices_y = [self.start_of_rect.top, self.start_of_rect.bottom,
                      self.end_of_rect.top, self.start_of_rect.bottom]

        vertices_x.sort()
        vertices_y.sort()

        return Rectangle(vertices_x[0], vertices_y[0],
                         vertices_x[-1], vertices_y[-1])


    def is_should_create_collision_rectangle(self, cycle: int, i: int, j: int, grid):
        return self.is_rect_started and (grid.is_passable(i, j) or self.is_next_side(cycle))

    def create_and_add_new_rectangle(self):
        self._collision_rectangles.append(self.get_new_rectangle())
        self.start_of_rect = None

    def save_this_tic_data(self, cycle: int, i: int, j: int, grid):
        self.old_cycle = cycle

        if self.start_of_rect is None and not grid.is_passable(i, j):
            self.start_of_rect = grid.get_collision_rect(i, j)

        self.end_of_rect = grid.get_collision_rect(i, j)

    def handle_cell(self, cycle: int, i: int, j: int,
                    arr: List[List[int]], grid) -> bool:
        if self.is_should_create_collision_rectangle(cycle, i, j, grid):
            self.create_and_add_new_rectangle()
        self.save_this_tic_data(cycle, i, j, grid)
        return True

    def bypass(self, arr: List[List[int]], grid):
        super().bypass(arr, grid)
        """
        из-за того, что обход заканчивается не поворотом 
        на следующий cycle, последний rectangle может быть 
        не сохранен. Нужно вызвать еще раз handle_cell
        """
        self.handle_cell(0, self.grid_rectangle._left_top_index[0],
                         self.grid_rectangle._left_top_index[1], arr, grid)

    def get_collision_rectangles(self, arr: List[List[int]], grid) -> List[Rectangle]:
        self.bypass(arr, grid)
        return self._collision_rectangles


class Room:
    def __init__(self, grid_rectangle: GridRectangle,
                arr_after_split: List[List[int]],
                grid):
        """
        :param grid: сетка
        """
        self._grid = grid


        self._grid_rectangle = grid_rectangle

        self.outer_rectangle = self.get_outer_rectangle(grid)
        self._collision_rectangles = self.get_collision_rectangles(grid)
        self.neighbours = self.get_all_neighbours(arr_after_split, grid)

    def get_all_neighbours(self, arr_after_split: List[List[int]], grid) -> \
                Tuple[List[int], List[int], List[int], List[int]]:
        group_of_neighour_rectangles = GroupOfRectangleNeighbours(self._grid_rectangle)
        result = group_of_neighour_rectangles.get_neighbours(arr_after_split, grid)
        return result

    def get_collision_rectangles(self, grid) -> List[Rectangle]:
        room_form = RoomFigureFormCreator(self._grid_rectangle)
        result = room_form.get_collision_rectangles(grid.arr, grid)
        return result


    def get_outer_rectangle(self, grid) -> Rectangle:
        grid_rectangle = self._grid_rectangle
        left_top_cell = grid.get_collision_rect(grid_rectangle.top_index,
                                                grid_rectangle.left_index)

        right_bottom_cell = grid.get_collision_rect(grid_rectangle.bottom_index,
                                                    grid_rectangle.right_index)

        return Rectangle(left_top_cell.left, left_top_cell.top,
            right_bottom_cell.right, right_bottom_cell.bottom)

    def is_intersect(self, seg: Segment) -> bool:
        for i in range(len(self._collision_rectangles)):
            rectangle = self._collision_rectangles[i]
            if intersect_seg_rect(seg, rectangle) is not None:
                return True
        return False

    def get_neighbours(self, seg: Segment) -> List[int]:
        edges = self.outer_rectangle.get_edges()
        result = []
        """
        порядок следования сторон совпадает с порядком следования
        neighbours, то есть по данному индексу стороне соответствует neighbour
        """
        for i in range(len(edges)):
            if intersect_segments(edges[i], seg) is not None:
                result += self.neighbours[i]

        return get_list_without_equal_elements(result)

    def draw_rect(self, COLOR: Tuple[int, int, int], LINE_WIDTH: int,
                  rectangle: Rectangle):
        dx = self._grid.scene.relative_center.x
        dy = self._grid.scene.relative_center.y

        draw.rect(self._grid.scene.screen, COLOR,
            (rectangle.left - dx, rectangle.top - dy, rectangle.width, rectangle.height), LINE_WIDTH)

    def draw_outer_rectangle(self):
        COLOR = (0, 255, 0)
        LINE_WIDTH = 10

        self.draw_rect(COLOR, LINE_WIDTH, self.outer_rectangle)

    def draw_collision_rectangles(self):
        COLOR = (255, 255, 255)
        LINE_WIDTH = 5

        for i in range(len(self._collision_rectangles)):
            self.draw_rect(COLOR, LINE_WIDTH, self._collision_rectangles[i])

    def process_draw(self):
        self.draw_outer_rectangle()
        self.draw_collision_rectangles()

class RoomsGraph:
    def __init__(self, rectangles: List[GridRectangle],
                arr_after_split: List[List[int]],
                grid):

        for i in range(len(rectangles)):
            tmp = ArrAfterSplitCorrecter(rectangles[i])
            tmp.correct_arr_after_split(arr_after_split, grid)

        self._grid = grid
        self._arr_after_split = arr_after_split
        self._used = IsMarkedManager(rectangles)
        self._rooms = self._get_all_rooms(rectangles)

    def _get_room_color_by_pos(self, pos: Point) -> int:
        i0, j0 = self._grid.get_index_by_pos(pos)
        color = self._arr_after_split[i0][j0]
        if not color:
            raise ValueError('отрезок не должен начинаться в стене')
        return color - 1

    def is_seg_intersect_wall(self, seg: Segment) -> bool:
        """
        Обход графа bfs'ом
        :param seg: отрезок, который проверяем
        :return: bool
        """
        self._used.next_iteration()

        color0 = self._get_room_color_by_pos(seg.p1)
        self._used.mark(color0)

        queue = deque()
        queue.append(color0)

        while len(queue):
            color = queue.popleft()
            room = self._rooms[color]

            if room.is_intersect(seg):
                return True

            neighbours = room.get_neighbours(seg)
            for i in range(len(neighbours)):
                neighbour_color = neighbours[i] - 1
                if self._used.is_marked(neighbour_color):
                    continue

                self._used.mark(neighbour_color)
                queue.append(neighbour_color)

        return False

    def _get_all_rooms(self, grid_rectangles: List[GridRectangle]) -> List[Room]:
        """
        на основе grid_rectangles формирует все комнаты.
        """
        result = []
        for i in range(len(grid_rectangles)):
            new_room = Room(grid_rectangles[i], self._arr_after_split, self._grid)
            result.append(new_room)

        return result

    def process_draw(self):
        """
        для debug

        отрисовывает внешние границы всех комнат одним из случайных цветов.
        """
        for i in range(len(self._rooms)):
            self._rooms[i].process_draw()
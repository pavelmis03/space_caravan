from typing import List
from enemy_interaction_with_grid.vision.rectangle_bypass.round_bypasser import RectangleBypasserAbstract
from geometry.rectangle import Rectangle
from geometry.optimized.rectangle import StaticRectangle
from geometry.point import Point
from map.level.rect.splitter import GridRectangle
from utils.list import delete_element

class CollisionFormCreator(RectangleBypasserAbstract):
    """
    Создает прямоугольники коллизий комнаты (объединяет несколько клеток стен в один прямоугольник).
    """
    def __init__(self, grid_rectangle: GridRectangle):
        super().__init__(grid_rectangle)
        self._collision_rectangles = []

        """
        start_of_rect и end_of_rect нужны, чтобы формировать на их основе прямоугольник коллизий. Сами представляют
        собой прямоугольники, т.к. это удобный способ хранить начало и конец прямоугольника. 
        """
        self._start_of_rect = None
        self._end_of_rect = None

        self._old_cycle = -1 # на каком цикле bypass мы находились прошлый тик.

    def _bypass(self, arr: List[List[int]], grid):
        """
        Обход grid_rectangle.
        из-за того, что обход заканчивается не поворотом на следующий cycle, последний rectangle может быть не сохранен.
        Нужно вызвать еще раз handle_cell
        """
        super()._bypass(arr, grid)
        self._handle_cell(0, self._grid_rectangle._left_top_index[0],
                          self._grid_rectangle._left_top_index[1], arr, grid)

    def _handle_cell(self, cycle: int, i: int, j: int,
                     arr: List[List[int]], grid) -> bool:
        """
        Обработка клетки. Здесь происходит логика создания прямоугольников коллизий.
        :return: True
        """
        if self._is_should_create_collision_rectangle(cycle, i, j, grid):
            self._create_and_add_new_rectangle()
        self._save_this_tic_data(cycle, i, j, grid)
        return True #никогда не нужно прерывать обход

    def _is_should_create_collision_rectangle(self, cycle: int, i: int, j: int, grid):
        """
        Нужно ли в этот тик создать прямоугольник коллизий.
        """
        return self._is_rect_started and (grid.is_passable(i, j) or self._is_next_side(cycle))

    def _create_and_add_new_rectangle(self):
        """
        Создает прямоугольник коллизий и добавляет его в список.
        """
        self._collision_rectangles.append(self._get_new_rectangle())
        self._start_of_rect = None

    def _save_this_tic_data(self, cycle: int, i: int, j: int, grid):
        """
        Сохраняет данные об этом тике. Пригодится в следующих тиках.
        """
        self._old_cycle = cycle

        if self._start_of_rect is None and not grid.is_passable(i, j):
            self._start_of_rect = grid.get_collision_rect(i, j)

        self._end_of_rect = grid.get_collision_rect(i, j)

    @property
    def _is_rect_started(self) -> bool:
        """
        Начали ли мы создание прямоугольника коллизий.
        """
        return self._start_of_rect is not None

    def _is_next_side(self, this_cycle: int) -> bool:
        """
        Перешли ли мы на следующую сторону обхода grid_rectangle
        """
        return self._old_cycle != this_cycle

    def _get_new_rectangle(self) -> StaticRectangle:
        """
        :return: прямоугольник коллизий на основе self._start_of_rect и self._end_of_rect
        """
        """
        Имеем start_of_rect и end_of_rect.
        
        Нужно составить Rectangle, который является выпуклой оболочкой
        для всех вершин обоих прямоугольников. Самый простой способ -
        отсортировать все значения и взять граничные.
        """
        vertices_x = [self._start_of_rect.left, self._start_of_rect.right,
                      self._end_of_rect.left, self._end_of_rect.right]
        vertices_y = [self._start_of_rect.top, self._start_of_rect.bottom,
                      self._end_of_rect.top, self._start_of_rect.bottom]

        vertices_x.sort()
        vertices_y.sort()

        return StaticRectangle(vertices_x[0], vertices_y[0], vertices_x[-1], vertices_y[-1])

    def get_collision_rectangles(self, arr: List[List[int]], grid) -> List[StaticRectangle]:
        """
        :return: Прямоугольники коллизий комнаты.
        """
        self._bypass(arr, grid)
        # после обхода возникают прямоугольники, полностью лежащие внутри других:
        deleter = UselessRectanglesDeleter(self._collision_rectangles)
        deleter.delete_useless_rectangles()

        return self._collision_rectangles


class UselessRectanglesDeleter:
    """
    Занимается удаление ненужных прямоугольников коллизий.
    """
    def __init__(self, collision_rectangles: List[Rectangle]):
        self._collision_rectangles = collision_rectangles

    def delete_useless_rectangles(self):
        """
        Удаляет прямоугольники коллиий, который лежат внутри других прямоугольников.
        """
        i = len(self._collision_rectangles) - 1
        while i >= 0 and len(self._collision_rectangles):
            if self._is_in_other_rect(i):
                delete_element(self._collision_rectangles, i)
            i -= 1

    def _is_in_other_rect(self, rect_index: int) -> bool:
        """
        Находится ли прямоугольник полностью внутри какого-то другого.
        """
        vertexes = self._collision_rectangles[rect_index].get_vertexes()
        for i in range(len(self._collision_rectangles)):
            if rect_index == i:
                continue
            if self._is_vertexes_inside_rect(vertexes, self._collision_rectangles[i]):
                return True
        return False

    def _is_vertexes_inside_rect(self, vertexes: List[Point], checker: Rectangle) -> bool:
        """
        Находятся ли все вершины внутри прямоугольника.
        """
        for k in range(len(vertexes)):
            if not checker.is_inside(vertexes[k]):
                return False
        return True
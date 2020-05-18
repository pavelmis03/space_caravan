from map.grid import Grid
from pygame import Surface, Rect
from utils.image import ImageManager
from drawable_objects.base import SurfaceObject
from geometry.point import Point


class GridDrawStaticManager(Grid):
    """
    Класс для оптимизации отрисовки статической графики.
    Принимает grid, отрисовывает все на 1 surface,
    далее бьет его на квадраты размером в половину экрана.

    Отрисовывает только те квадраты, которые на экране (как в обычном grid).

    Это ускоряет отрисовку, так как все объекты уже заранее отрендерины.
    Более отрисовка вызывается всего 9 раз (так как полученных квадратов на экране
    не больше 9).
    """

    def __init__(self, grid: Grid):
        cell_width = int(grid.scene.width / 2)
        cell_height = int(grid.scene.height / 2)
        """
        Прибавляем cell_width - 1 и cell_height - 1
        для деления с округленим вверх        
        """
        arr_width = int((grid.width + cell_width - 1) / cell_width)
        arr_height = int((grid.height + cell_height - 1) / cell_height)

        super().__init__(grid.scene, grid.controller, grid.pos)
        self._fill_arr(0, cell_width, cell_height, arr_width, arr_height)

        full_grid_surface = self.pre_render_all(grid)
        self.split_on_frames(full_grid_surface)

    def pre_render_all(self, grid: Grid) -> Surface:
        """
        Отрисовывает всё на 1 surface

        Чтобы не было проблем в расчетах, прибавляет
        cell_width и cell_height к размеру всего поля
        """
        self.surface_width = grid.width + self.cell_width
        self.surface_height = grid.height + self.cell_height
        res = Surface((self.surface_width, self.surface_height))
        for i in range(len(grid.arr)):
            for j in range(len(grid.arr[i])):
                sprite = grid.arr[i][j]
                ImageManager.process_draw(sprite.image_name, sprite.pos - self.pos,
                                          res, sprite.zoom, sprite.angle)
        return res

    def split_on_frames(self, surface: Surface):
        """
        бьет полученную surface на квадраты, чтобы отрисовывать только то,
        что на экране
        """
        frame_rect = Rect(0, 0, self.cell_width, self.cell_height)
        pos_offset = Point((self.cell_width) / 2, (self.cell_height) / 2)
        """
        учитываем смещение прямоугольников
        """
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                """
                не нужно делать проверку на выход за пределы, 
                так как мы прибавили cell_width и cell_height
                к размеру всего поля
                """
                frame_rect.x = j * self.cell_width
                frame_rect.y = i * self.cell_height

                self.arr[i][j] = SurfaceObject(surface.subsurface(frame_rect),
                                               self.scene, self.controller,
                                               self.pos + Point(frame_rect.x, frame_rect.y) + pos_offset)

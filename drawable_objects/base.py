import pygame

from geometry.point import Point
from controller.controller import Controller
from scenes.base import Scene
from utils.image import ImageManager

from math import cos
from math import sin


class AbstractObject:
    """
        Базовый класс неотрисовымаевого объекта, но содержащего отрисовывательные элементы

        :param scene: сцена объекта
        :param controller: ссылка на объект контроллера
        :param pos: координаты объекта
        """
    def __init__(self, scene: Scene, controller: Controller):
        self.scene = scene
        self.controller = controller

    def process_logic(self):
        """
        Исполнение логики объекта.
        """
        pass

    def process_draw(self):
        """
        Отрисовка объекта.
        """
        pass

class SurfaceObject(AbstractObject):
    """
    Отдельный класс для отрисовки уже отреднеренного surface.
    Используется для отрисовки статичной предподсчитанной графики (то есть той, которая
    не двигается. Не стоит путать со SpriteObject. Он не двигается относительно экрана).

    Не нужно его использовать для других целей, он хранит
    в себе картинку, а значит потребляет много памяти.
    """
    def __init__(self, surface: pygame.Surface, scene: Scene, controller: Controller, pos: Point):
        super().__init__(scene, controller)
        self.surface = surface
        self.pos = pos

    def process_draw(self):
        relative_center = self.scene.relative_center
        relative_pos = self.pos - relative_center
        ImageManager.draw_surface(self.surface, relative_pos, self.scene.screen)

class DrawableObject(AbstractObject):
    """
    Базовый класс отрисовываемого объекта.

    :param scene: сцена объекта
    :param controller: ссылка на объект контроллера
    :param pos: координаты объекта
    """
    def __init__(self, scene: Scene, controller: Controller, pos: Point):
        super().__init__(scene, controller)
        self.pos = pos


    def move(self, new_pos):
        """
        Перемещение объекта.

        :param new_pos: новое положение
        """
        self.pos = new_pos


class SpriteObject(DrawableObject):
    """
    Базовый класс объекта с текстурой.

    :param scene: сцена объекта
    :param controller: ссылка на объект контроллера (пока None)
    :param image_name: имя картинки в базе менеджера
    :param pos: координаты объекта
    :param angle: угол поворота объекта
    :param zoom: масштаб картинки
    """
    def __init__(self, scene: Scene, controller: Controller, image_name: str,
                 pos: Point, angle: float = 0, zoom: float = 1):
        super().__init__(scene, controller, pos)
        self.image_name = image_name
        self.angle = angle
        self.zoom = zoom

    def process_draw(self):
        ImageManager.process_draw(self.image_name, self.pos, self.scene.screen, self.zoom, self.angle)

    def collides_with(self, other_object):
        """
        Проверка на коллизию через pygame. Вроде бесполезно, но пока оставим.

        :param other_object: другой объект для проверки на коллизию
        """
        return pygame.sprite.collide_mask(self, other_object)


class GameSprite(SpriteObject):
    """
    Базовый класс объекта на игровом уровне

    :param scene: сцена объекта
    :param controller: ссылка на объект контроллера (пока None)
    :param image_name: имя картинки в базе менеджера
    :param pos: координаты объекта
    :param angle: угол поворота объекта
    :param zoom: масштаб картинки
    """
    def __init__(self, scene: Scene, controller: Controller, image_name: str, pos: Point, angle: float = 0,
                 zoom: float = 1):
        super().__init__(scene, controller, image_name, pos, angle, zoom)
        self.scene.plane.insert(self, self.pos)
        self.enabled = True
        self.rotation_offset = None

    def destroy(self):
        """
        Уничтожение игрового объекта. Будет уничтожен на ближайшей итерации своей сценой.
        """
        self.enabled = False

    def process_draw(self):
        """
        Отрисовка объекта в относительных координатах

        Если объект вне экрана, он не отрисовывается
        relative_center: центр относительных координат
        """
        relative_center = self.scene.relative_center
        relative_pos = self.pos - relative_center

        if ImageManager.is_out_of_screen(self.image_name, self.zoom,
                                         relative_pos, self.scene.game.screen_rectangle):
            return

        ImageManager.process_draw(self.image_name, relative_pos, self.scene.screen, self.zoom, self.angle, self.rotation_offset)

    def move(self, new_pos):
        self.scene.plane.do_step(self, self.pos, new_pos)
        self.pos = new_pos


class MovingGameSprite(GameSprite):
    """
    Для движения по направлению self.angle
    """
    def __init__(self, scene: Scene, controller: Controller, image_name: str,
                 pos: Point, speed: float, angle: float = 0, zoom: float = 1):
        super().__init__(scene, controller, image_name, pos, angle, zoom)
        self.speed = speed

    def get_direction_vector(self) -> Point:
        """
        Не учитывает коллизи и т.п.
        """
        x_speed = cos(self.angle) * self.speed
        y_speed = -sin(self.angle) * self.speed
        return Point(x_speed, y_speed)

class Humanoid(MovingGameSprite):
    HITBOX_RADIUS = 25

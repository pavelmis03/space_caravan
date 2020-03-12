import pygame

from geometry.point import Point
from controller.controller import Controller
from scenes.base import Scene
from utils.image import ImageManager


class DrawableObject:
    """
    Базовый класс отрисовываемого объекта.

    :param scene: сцена объекта
    :param controller: ссылка на объект контроллера
    :param pos: координаты объекта
    """
    def __init__(self, scene: Scene, controller: Controller, pos: Point):
        self.scene = scene
        self.controller = controller
        self.pos = pos

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

    def move(self, new_pos):
        """
        Перемещение объекта

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
    """
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

        ImageManager.process_draw(self.image_name, relative_pos, self.scene.screen, self.zoom, self.angle)

from utils.image import ImageManager

import pygame

from geometry.point import Point
from controller.controller import Controller
from scenes.base import Scene

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
    """
    def __init__(self, scene: Scene, controller: Controller, image_str: str,
                 pos: Point, angle: float = 0, resize_percents: float = 1):
        """
        :param scene:
        :param controller:
        :param image_str:
        :param pos:
        :param angle:
        :param resize_percents:
        """
        super().__init__(scene, controller, pos)
        self.image = image_str
        self.resize_percents = resize_percents
        self.angle = angle

    def process_draw(self):
        ImageManager.process_draw(self.image, self.pos, self.scene.screen,
                                  self.resize_percents, self.angle)

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
    def is_out_of_screen(self, rel_pos: Point, w: float, h: float):
        left = rel_pos.x - w / 2
        top = rel_pos.y - h / 2
        right = rel_pos.x + w / 2
        bottom = rel_pos.y + h / 2

        if right < 0 or bottom < 0 or \
            left > self.scene.game.width or \
            top > self.scene.game.height:
            return True
        return False

    def process_draw(self):
        """
        Отрисовка объекта в относительных координатах

        Если объект вне экрана, он не отрисовывается
        relative_center: центр относительных координат
        """
        relative_center = self.scene.relative_center
        relative_pos = self.pos - relative_center

        w = ImageManager.get_width(self.image, self.resize_percents)
        h = ImageManager.get_height(self.image, self.resize_percents)
        if self.is_out_of_screen(relative_pos, w, h):
            return

        old_pos = self.pos
        self.pos = relative_pos
        super().process_draw()
        self.pos = old_pos




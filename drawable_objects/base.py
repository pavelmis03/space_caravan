from math import atan2, degrees

import pygame

from geometry.point import Point

class DrawableObject:
    """
    Базовый класс отрисовываемого объекта.

    :param scene: сцена объекта
    :param controller: ссылка на объект контроллера
    :param pos: координаты объекта
    """
    def __init__(self, scene, controller, pos):
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
    :param filename: имя файла с текстурой
    :param pos: координаты объекта
    :param rot: угол поворота объекта
    """
    def __init__(self, scene, controller, filename, pos, angle):
        super().__init__(scene, controller, pos)
        self.image = pygame.image.load(filename)
        self.rotated_image = self.image
        self.rotate(angle)

    def resize(self, percents):
        """
        Изменить размер текстуры в заданное число раз.

        :param percents: доля исходного размера (десятичная дробь)
        """
        rect = self.image.get_rect()
        size = (
            int(rect.width * percents),
            int(rect.height * percents)
        )
        self.image = pygame.transform.scale(self.image, size)

    def rotate(self, new_angle):
        """
        Задать объекту желаемый игол поворота.

        :param new_angle: новый угол поворота
        :return:
        """
        self.angle = new_angle
        self.rotated_image = pygame.transform.rotate(self.image, degrees(self.angle))

    def process_draw(self):
        rect = self.rotated_image.get_rect()
        rect.center = (self.Point.x, self.Point.y)
        self.scene.screen.blit(self.rotated_image, rect)

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
    def process_draw(self, relative_center):
        """
        Отрасовка объекта в относительных координатах

        :param relative_center: центр относительных координат
        """
        rect = self.rotated_image.get_rect()
        relative_pos = self.pos - relative_center
        rect.center = (relative_pos.x, relative_pos.y)
        self.scene.screen.blit(self.rotated_image, rect)

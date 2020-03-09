"""
Все, что связано с логикой отрисовки
"""
import pygame
from math import degrees
from geometry.point import Point

class ImageManager:
    images = {} # получить по ключу pygame картинку

    @staticmethod
    def load_all():
        """
        по умолчанию считает, что все картинки png. Ключ должен
        совпадать с названием картинки.

        :return:
        """
        img_names = ['player', 'floor', 'wall']
        for i in range(len(img_names)):
            ImageManager.images[img_names[i]] = pygame.image.load('images/' + img_names[i] + '.png')

    @staticmethod
    def process_draw(img_str: str, pos_center: Point, screen,
                     resize_percents: float, rotate_angle: float):
        image = ImageManager.images[img_str]
        image = ImageManager.resize(image, resize_percents)
        image = ImageManager.rotate(image, rotate_angle)

        rect = image.get_rect()
        rect.center = (pos_center.x, pos_center.y)
        screen.blit(image, rect)

    @staticmethod
    def resize(image, percents: float):
        """
        Изменить размер текстуры в заданное число раз.

        :param percents: доля исходного размера (десятичная дробь)
        """
        if percents == 1:
            return image

        rect = image.get_rect()
        size = (
            int(rect.width * percents),
            int(rect.height * percents)
        )
        return pygame.transform.scale(image, size)

    @staticmethod
    def rotate(image, angle: float):
        """
        Задать объекту желаемый угол поворота.

        :param new_angle: новый угол поворота
        """
        if not angle:
            return image
        return pygame.transform.rotate(image, degrees(angle))

    @staticmethod
    def get_width(image_str: str, percents: float) -> float:
        return ImageManager.images[image_str].get_width() * percents

    @staticmethod
    def get_height(image_str: str, percents: float) -> float:
        return ImageManager.images[image_str].get_height() * percents


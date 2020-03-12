"""
Все, что связано с логикой отрисовки
"""
import pygame
from math import degrees
from geometry.point import Point
from geometry.rectangle import intersect, Rectangle

class ImageManager:
    images = {} # получить по ключу pygame картинку
    IMG_NAMES = ['player', 'floor', 'wall']
    @staticmethod
    def load_all():
        """
        по умолчанию считает, что все картинки png. Ключ должен
        совпадать с названием картинки.

        :return:
        """

        for i in range(len(ImageManager.IMG_NAMES)):
            ImageManager.images[ImageManager.IMG_NAMES[i]] = \
                pygame.image.load('images/' + ImageManager.IMG_NAMES[i] + '.png')

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
    def is_out_of_screen(image_name: str, zoom: float,
                         relative_pos: Point, screen_rectangle: Rectangle):
        """
        relative_pos - координаты относительно центра экрана.

        если прямоугольник картинки не пересекается с прямоугольником экрана(и не находится
        внутри), то картинка все экрана.
        :param image_name:
        :param zoom:
        :param relative_pos:
        :return:
        """
        w = ImageManager.get_width(image_name, zoom)
        h = ImageManager.get_height(image_name, zoom)
        rectangle = Rectangle(0, 0, w, h)
        rectangle.center = relative_pos
        return intersect(rectangle, screen_rectangle).is_empty()

    @staticmethod
    def get_width(image_str: str, percents: float) -> float:
        return ImageManager.images[image_str].get_width() * percents

    @staticmethod
    def get_height(image_str: str, percents: float) -> float:
        return ImageManager.images[image_str].get_height() * percents



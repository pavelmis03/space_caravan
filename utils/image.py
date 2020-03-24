"""
Все, что связано с логикой отрисовки
"""
import pygame
from math import degrees
from geometry.point import Point
from geometry.rectangle import intersect, Rectangle

class ImageManager:
    images = {} # получить по ключу pygame картинку
    IMG_NAMES = ['player', 'floor', 'wall', 'bullet']
    @staticmethod
    def load_all():
        """
        по умолчанию считает, что все картинки png. Ключ должен
        совпадать с названием картинки.
        """
        for i in range(len(ImageManager.IMG_NAMES)):
            ImageManager.load_img(ImageManager.IMG_NAMES[i])

    @staticmethod
    def load_img(img_name: str):
        ImageManager.images[img_name] = \
            pygame.image.load(ImageManager.img_name_to_path(img_name))

    @staticmethod
    def img_name_to_path(img_name: str) -> str:
        return 'images/' + img_name + '.png'

    @staticmethod
    def draw_surface(surface: pygame.Surface, pos_center: Point, screen):
        rect = surface.get_rect()
        rect.center = (pos_center.x, pos_center.y)
        screen.blit(surface, rect)

    @staticmethod
    def process_draw(img_str: str, pos_center: Point, screen,
                     resize_percents: float, rotate_angle: float, rotate_offset: list=None):
        image = ImageManager.images[img_str]
        image = ImageManager.resize(image, resize_percents)
        image = ImageManager.rotate(image, rotate_angle, rotate_offset)

        ImageManager.draw_surface(image, pos_center, screen)

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
    def rotate(image, angle: float, rotate_offset=None):
        """
        Задать объекту желаемый угол поворота.

        :param image: поворачиваемая картинка
        :param angle: новый угол поворота
        :param rotate_offset: оффсет относительно центра для точки поворота
        """
        if not angle:
            return image
        if not rotate_offset:
            rotate_offset = image.get_rect().center
        w, h = image.get_size()
        img = pygame.Surface((w*2, h*2), pygame.SRCALPHA)
        img.blit(image, (w - rotate_offset[0], h - rotate_offset[1]))
        return pygame.transform.rotate(img, degrees(angle))

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



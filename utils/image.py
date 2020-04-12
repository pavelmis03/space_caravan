"""
Все, что связано с логикой отрисовки
"""
import os

import pygame
from math import degrees
from geometry.point import Point
from geometry.rectangle import intersect, Rectangle


class ImageManager:
    """
    Загружает все картинки и осуществляет быстрый доступ к ним а так же работу с ними
    Возможна рекурсивная загруска всех png картинок
    """
    images = {}  # получить по ключу pygame картинку
    IMAGE_PATH = 'images'

    @staticmethod
    def load_all():
        """
        по умолчанию считает, что все картинки png.
        """
        ImageManager.load_dir(ImageManager.IMAGE_PATH)

    @staticmethod
    def load_dir(directory: str):
        """
        Загрузка всех png изображений из директории рекурсивно
        :param directory: директория
        """
        for item in os.listdir(directory):
            full_item = os.path.join(directory, item)
            short_dir = directory.replace(ImageManager.IMAGE_PATH, '').strip(os.sep)
            if os.path.isdir(full_item):
                manager_dir = ImageManager.get_image(short_dir, os.sep)
                manager_dir[item] = {}
                ImageManager.load_dir(full_item)
            elif '.png' in item:
                manager_dir = ImageManager.get_image(short_dir, os.sep)
                item = item.replace('.png', '')
                manager_dir[item] = pygame.image.load(full_item)

    @staticmethod
    def get_image(path: str, delimiter: str = '.'):
        """
        Данная функция нужна для удобного получения изображений из
        ImageManager.images
        Может так же и возвращать словари с изображениями при указании неполного пути

        :param path: путь до изображения, выглядит примерно как
            папка.папка.файл (файл без расширения, начало папок из images)
        :param delimiter: разделитель между папками и изображениями
            по умолчанию используется точка (aka python style),
            но можно и делить по другому, слешы крайне НЕ рекомендуются
        """
        res = ImageManager.images
        if not path:
            return res
        for item in path.split(delimiter):
            if item in res:
                res = res[item]
            else:
                raise ValueError(item + ' not found in path ' + path)
        return res

    @staticmethod
    def draw_surface(surface: pygame.Surface, pos_center: Point, screen):
        rect = surface.get_rect()
        rect.center = (pos_center.x, pos_center.y)
        screen.blit(surface, rect)

    @staticmethod
    def process_draw(img_str: str, pos_center: Point, screen,
                     resize_percents: float, rotate_angle: float, rotate_offset: list = None):
        image = ImageManager.get_image(img_str)
        if isinstance(image, dict):
            raise ValueError(img_str + ' is a dir, not a file')
        image = ImageManager.resize(image, resize_percents)
        image = ImageManager.rotate(image, rotate_angle, rotate_offset)

        ImageManager.draw_surface(image, pos_center, screen)

    @staticmethod
    def resize(image: pygame.Surface, percents: float) -> pygame.Surface:
        """
        Изменить размер текстуры в заданное число раз.

        :param image: текстура, размер которой будет изменен
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
    def rotate(image: pygame.Surface, angle: float, rotate_offset=None) -> pygame.Surface:
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
        img = pygame.Surface((w * 2, h * 2), pygame.SRCALPHA)
        img.blit(image, (w - rotate_offset[0], h - rotate_offset[1]))
        return pygame.transform.rotate(img, degrees(angle))

    @staticmethod
    def is_out_of_screen(image_name: str, zoom: float,
                         relative_pos: Point, screen_rectangle: Rectangle):
        """
        relative_pos - координаты относительно центра экрана.

        если прямоугольник картинки не пересекается с прямоугольником экрана(и не находится
        внутри), то картинка все экрана.
        :param screen_rectangle: прямоугольник, задающий размеры экрана
        :param image_name: название картинки (путь до нее)
        :param zoom: во сколько раз увеличить картинку, если нужно
        :param relative_pos: позиция относительно окна
        :return:
        """
        w = ImageManager.get_width(image_name, zoom)
        h = ImageManager.get_height(image_name, zoom)
        rectangle = Rectangle(0, 0, w, h)
        rectangle.center = relative_pos
        return intersect(rectangle, screen_rectangle).is_empty()

    @staticmethod
    def get_width(image_str: str, percents: float) -> float:
        """
        Получить длинну изображения
        :param image_str: название картинки (путь до нее)
        :param percents: во сколько раз увеличить картинку, если нужно
        :return: длинна изображения
        """
        image = ImageManager.get_image(image_str)
        if isinstance(image, dict):
            raise ValueError(image_str + ' is a dir, not a file')
        return image.get_width() * percents

    @staticmethod
    def get_height(image_str: str, percents: float) -> float:
        """
        Получить высоту изображения
        :param image_str: название картинки (путь до нее)
        :param percents: во сколько раз увеличить картинку, если нужно
        :return: высота изображения
        """
        image = ImageManager.get_image(image_str)
        if isinstance(image, dict):
            raise ValueError(image_str + ' is a dir, not a file')
        return image.get_height() * percents

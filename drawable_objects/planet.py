import pygame

from geometry.point import Point
from scenes.base import Scene
from constants import Color
from controller.controller import Controller
from drawable_objects.base import DrawableObject, SpriteObject
from drawable_objects.text import Text
from utils.image import ImageManager


class Planet(SpriteObject):
    """
    Объект планеты на звездной карте

    :param scene: сцена объекта
    :param controller: ссылка на объект контроллера
    :param image_name: имя картинки в базе менеджера
    :param pos: координаты объекта
    :param angle: угол поворота объекта
    :param zoom: масштаб картинки
    :param kwargs: именованные аргументы процедуры, вызываемой по нажатию

    :param planet_biom: запуск карты определенного биома планеты (не реализовано)
    :param planet_name: название планеты (не реализовано)
    """

    def __init__(self, scene: Scene, controller: Controller, image_name: str,
                 pos: Point, angle: float = 0, zoom: float = 1,function=None, kwargs={}, planet_biom = 'None', planet_name = 'Test'):
        super().__init__(scene, controller, image_name, pos, angle, zoom)
        self.function = function
        self.kwargs = kwargs
        self.name = planet_name
        self.biom = planet_biom
        self.enabled = True
        self.rotation_offset = [0, 0]



    def process_logic(self):
        click_pos = self.controller.get_click_pos()
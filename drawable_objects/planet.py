from math import pi
from random import random

from geometry.circle import Circle
from geometry.point import Point
from scenes.base import Scene
from controller.controller import Controller
from drawable_objects.base import SpriteObject


class Planet(SpriteObject):
    """
    Объект планеты на звездной карте

    :param scene: сцена объекта
    :param controller: ссылка на объект контроллера
    :param image_name: имя картинки в базе менеджера
    :param pos: координаты объекта
    :param angle: угол поворота объекта
    :param zoom: масштаб картинки

    :param planet_biom: запуск карты определенного биома планеты (не реализовано)
    :param planet_name: название планеты (не реализовано)
    """
    BUTTON_RADIUS = 50
    IMAGE_ZOOM = 0.07
    BIOMS = ['Simple']
    IMAGE_NAMES = {
        'Simple': 'level_objects.planet'
    }

    def __init__(self, scene: Scene, controller: Controller, pos: Point,
                 planet_biom=BIOMS[0], planet_name='Test'):
        super().__init__(scene, controller, Planet.IMAGE_NAMES[planet_biom], pos,
                         random() * 2 * pi, Planet.IMAGE_ZOOM)
        self.geometry = Circle(pos, Planet.BUTTON_RADIUS)
        self.rotation_offset = [0, 0]
        self.name = planet_name
        self.biom = planet_biom
        self.enabled = True

    def process_logic(self):
        click_pos = self.controller.get_click_pos()

        if click_pos and self.geometry.is_inside(click_pos):
            pass

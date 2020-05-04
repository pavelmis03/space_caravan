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
    :param pos: координаты объекта
    :param biom: биом - вид планеты
    :param name: название планеты
    """
    BUTTON_RADIUS = 50
    IMAGE_ZOOM = 0.07
    BIOMS = ['Simple']
    IMAGE_NAMES = {
        'Simple': 'level_objects.planet'
    }

    def __init__(self, scene: Scene, controller: Controller, pos: Point, biom=BIOMS[0], name='Test'):
        super().__init__(scene, controller, Planet.IMAGE_NAMES[biom], pos, random() * 2 * pi, Planet.IMAGE_ZOOM)
        self.geometry = Circle(pos, Planet.BUTTON_RADIUS)
        self.rotation_offset = [0, 0]
        self.name = name
        self.biom = biom
        self.enabled = True

    def process_logic(self):
        click_pos = self.controller.get_click_pos()

        if click_pos and self.geometry.is_inside(click_pos):
            pass

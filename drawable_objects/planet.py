import pygame

from math import pi
from random import random
from typing import Dict

from constants.planets_generation import ESTIMATED_SPACE_SIZE
from constants.color import COLOR
from geometry.circle import Circle
from geometry.point import Point, point_to_tuple
from scenes.base import Scene
from controller.controller import Controller
from drawable_objects.base import SpriteObject


class Planet(SpriteObject):
    """
    Объект планеты во всех смыслах: и в структуре игрового мира, и на космической карте.

    Для того, чтобы карту можно было масштабировать, планета хранит расчетную позицию и расчетный размер экрана.
    В логике по текущему размеру окна пересчитывается реальное положение планеты на экране (self.pos).

    :param scene: сцена объекта
    :param controller: ссылка на объект контроллера
    :param estimated_pos: расчетная позиция планеты на экране фиксированного размера
    :param biom: биом - вид планеты
    :param name: название планеты
    """
    BUTTON_RADIUS = 35
    BIOM_NAMES = [
        'Simple',
        'Ice',
        'Lava',
        'Violet',
        'Mushroom',
    ]
    IMAGES = [
        ('spacemap.simple_planet', 0.07),
        ('spacemap.ice_planet', 0.35),
        ('spacemap.lava_planet', 0.3),
        ('spacemap.violet_planet', 0.3),
        ('spacemap.mushroom_planet', 0.3),
    ]
    COUNTER = 0

    def __init__(self, scene: Scene, controller: Controller, estimated_pos: Point, biom=0, name='Test'):
        super().__init__(scene, controller, Planet.IMAGES[biom][0], Point(
        ), random() * 2 * pi, Planet.IMAGES[biom][1])
        self.rotation_offset = [0, 0]
        self.estimated_pos = estimated_pos
        self.update_real_pos()
        self.name = name
        self.biom = biom
        self.enabled = True
        self.chosen = False
        self.index = str(Planet.COUNTER)
        Planet.COUNTER += 1

        self.scene.common_data.planet_biom[self.index] = self.biom
        self.scene.common_data.planet_completed[self.index] = False

    def from_dict(self, data_dict: Dict):
        """
        Воспроизведение планеты из словаря.
        """
        super().from_dict(data_dict)
        self.estimated_pos.from_dict(data_dict['estimated_pos'])
        self.update_real_pos()
        self.name = data_dict['name']
        self.biom = data_dict['biom']
        self.image_name = self.IMAGES[self.biom][0]
        self.zoom = self.IMAGES[self.biom][1]
        self.index = data_dict['index']

    def to_dict(self) -> Dict:
        """
        Запись характеристик планеты в виде словаря.
        """
        result = super().to_dict()
        result.update({
            'estimated_pos': self.estimated_pos.to_dict(),
            'name': self.name,
            'biom': self.biom,
            'index': self.index,
        })
        return result

    def update_real_pos(self):
        """
        Перерасчет реальной позиции планеты на экране по постоянной расчетной позиции, расчетному размеру экрана
        и текущему размеру окна.
        """
        screen_size = list(self.scene.game.size)
        screen_size[1] -= self.scene.PANEL_HEIGHT
        scale_k = [screen_size[_i] / ESTIMATED_SPACE_SIZE[_i]
                   for _i in range(2)]
        self.pos = Point(scale_k[0] * self.estimated_pos.x,
                         scale_k[1] * self.estimated_pos.y)

    def run_level(self):
        """
        Запуск уровня. Именно здесь создается сцена уровня, так работает загрузка сцен.
        """
        from scenes.game.main import MainScene  # В обход цикличеких import'ов
        level_scene = MainScene(self.scene.game, self.index)
        self.scene.game.set_scene(level_scene)

    def process_draw(self):
        if self.chosen:
            integer_pos = (round(self.pos.x), round(self.pos.y))
            pygame.draw.circle(self.scene.screen, COLOR['RED'], integer_pos, self.BUTTON_RADIUS)
        super().process_draw()

    def process_logic(self):
        self.update_real_pos()
        geometry = Circle(self.pos, Planet.BUTTON_RADIUS)
        click_pos = self.controller.get_click_pos()
        if click_pos:
            self.chosen = geometry.is_inside(click_pos)

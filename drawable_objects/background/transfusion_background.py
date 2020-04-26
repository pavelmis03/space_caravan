"""
Неиспользуемый модуль. Может, позже пригодится.
"""
from drawable_objects.base import DrawableObject
from drawable_objects.background.rgb import RGB
from utils.simple_math import sign
from pygame import draw
from typing import Tuple
from geometry.point import Point
from controller.controller import Controller
from scenes.base import Scene


class TransfusionBackground(DrawableObject):
    """
    Фон, который переливается со временем.
    """

    def __init__(self, scene: Scene, controller: Controller, pos: Point,
                 colors=Tuple[RGB]):
        super().__init__(scene, controller, pos)
        self.colors = colors
        self.this_color = self.colors[0]
        self.next_color_index = 1

    def step_to_next_color(self):
        dt = self.colors[self.next_color_index] - self.this_color
        self.this_color += RGB(sign(dt.r), sign(dt.g), sign(dt.b), sign(dt.a))

    def select_next_color(self):
        self.next_color_index = (self.next_color_index + 1) % len(self.colors)

    def process_logic(self):
        self.step_to_next_color()
        if self.this_color == self.colors[self.next_color_index]:
            self.select_next_color()

    def process_draw(self):
        draw.rect(self.scene.screen, self.this_color.tuple,
                  (self.pos.x, self.pos.y, self.scene.game.width, self.scene.game.height), 0)

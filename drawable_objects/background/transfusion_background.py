from drawable_objects.base import DrawableObject
from drawable_objects.background.rgb import RGB
from utils.sign import sign
from pygame import draw
from typing import Tuple
from geometry.point import Point
from controller.controller import Controller
from scenes.base import Scene


class TransfusionBackground(DrawableObject):
    """
    Фон, который переливается со временем.
    Используется в dungeon для заполнения того,
    что за пределами экрана
    """
    def __init__(self, scene: Scene, controller: Controller, pos: Point,
                 colors = Tuple[RGB]):
        super().__init__(scene, controller, pos)
        self.colors = colors
        self.this_color = self.colors[0]
        self.next_color_index = 1

    def process_logic(self):
        dt = self.colors[self.next_color_index] - self.this_color
        self.this_color += RGB(sign(dt.r), sign(dt.g), sign(dt.b))
        if self.this_color == self.colors[self.next_color_index]:
            self.next_color_index = (self.next_color_index + 1) % len(self.colors)

    def process_draw(self):
        draw.rect(self.scene.screen, self.this_color.tuple,
                  (self.pos.x, self.pos.y, self.scene.game.width, self.scene.game.height), 0)
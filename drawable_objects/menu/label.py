from typing import Tuple

from drawable_objects.menu.text import Text
from scenes.base import Scene
from geometry.point import Point
from geometry.rectangle import tuple_to_rectangle
from constants.color import COLOR


class Label(Text):
    def pos_align_left(self) -> Point:
        return self.geometry.top_left

    def pos_align_center(self) -> Point:
        return self.geometry.center

    ALIGNS = {
        'left': pos_align_left,
        'center': pos_align_center,
    }
    FONT_NAME = 'zelekbold'

    def __init__(self, scene: Scene, geometry: Tuple, text: str, align: str):
        self.geometry = tuple_to_rectangle(geometry)
        super().__init__(scene, self.ALIGNS[align](self), text, COLOR['BLACK'], align, self.FONT_NAME,
                         self.geometry.height, False, False)

    def move(self, movement):
        self.geometry.move(movement)
        self.pos += movement

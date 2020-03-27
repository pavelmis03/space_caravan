import pygame

from constants.color import Color
from drawable_objects.base import DrawableObject
from drawable_objects.text import Text
from geometry.point import Point
from geometry.rectangle import tuple_to_rectangle, rectangle_to_rect


class Entry(DrawableObject):
    """ simple text box class for console """
    BG_COLOR = Color.BLACK
    BORDER_COLOR = Color.WHITE
    TEXT_COLOR = Color.WHITE
    TEXT_SHIFT = Point(3, 3)
    FONT_NAME = "Consolas"

    def __init__(self, scene, controller, geometry, initial_text="", font_size=20, visible=True, width_limit=None):
        self.geometry = tuple_to_rectangle(geometry)
        super().__init__(scene, controller, self.geometry.center)
        self.text = Text(scene, self.geometry.top_left + Entry.TEXT_SHIFT,
                         initial_text, Entry.TEXT_COLOR, 'left', Entry.FONT_NAME,
                         font_size, is_bold=False, width_limit=width_limit)
        self.visible = visible

    def process_draw(self):
        if not self.visible: return;
        pygame.draw.rect(self.scene.screen, Entry.BG_COLOR, rectangle_to_rect(self.geometry))
        pygame.draw.rect(self.scene.screen, Entry.BORDER_COLOR, rectangle_to_rect(self.geometry), 1)
        self.text.process_draw()

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True
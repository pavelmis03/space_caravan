import pygame

from constants import Color
from drawable_objects.base import DrawableObject
from drawable_objects.text import Text
from geometry.rectangle import rectangle_to_rect, tuple_to_rectangle


class Button(DrawableObject):
    BG_COLOR = Color.YELLOW
    BG_HOVER_COLOR = Color.ORANGE
    TEXT_COLOR = Color.CYAN
    TEXT_HOVER_COLOR = Color.BLUE
    FONT_NAME = 'Consolas'

    def __init__(self, scene, controller, geometry, text='Test', function=None,
                 function_args=None, font_size=20):
        self.geometry = tuple_to_rectangle(geometry)
        super().__init__(scene, controller, self.geometry.center)
        self.function = function
        self.function_args = function_args
        self.hover = False
        self.text = Text(scene, self.geometry.center, text, Button.TEXT_COLOR, 'center', Button.FONT_NAME, font_size)
        self.hover_text = Text(scene, self.geometry.center, text, Button.TEXT_HOVER_COLOR, 'center', Button.FONT_NAME,
                               font_size)

    def process_logic(self):
        self.hover = self.geometry.in_inside(self.controller.get_mouse_pos())
        click_pos = self.controller.get_click_pos()
        if click_pos and self.geometry.in_inside(click_pos):
            if self.function_args:
                self.function(self.function_args)
            else:
                self.function()

    def process_draw(self):
        if self.hover:
            bg_color = Button.BG_HOVER_COLOR
            text = self.hover_text
        else:
            bg_color = Button.BG_COLOR
            text = self.text
        pygame.draw.rect(self.scene.screen, bg_color, rectangle_to_rect(self.geometry))
        text.process_draw()
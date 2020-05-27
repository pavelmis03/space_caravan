import pygame

from typing import Tuple

from scenes.base import Scene
from controller.controller import Controller
from drawable_objects.base import DrawableObject
from geometry.rectangle import tuple_to_rectangle, rectangle_to_rect
from drawable_objects.text import Text


class TextBox(DrawableObject):
    PROMPT_TEXT_COLOR = (100, 100, 100)
    MAIN_TEXT_COLOR = (0, 0, 0)
    FONT_NAME = 'Consolas'
    BG_COLOR = (255, 255, 255)

    def __init__(self, scene: Scene, controller: Controller, geometry: Tuple, prompt_str: str):
        self.geometry = tuple_to_rectangle(geometry)
        super().__init__(scene, controller, self.geometry.center)
        self.font_size = round(self.geometry.height)
        self.prompt_str = prompt_str
        self.main_str = ''
        self.prompt_text = Text(scene, self.geometry.top_left, prompt_str, self.PROMPT_TEXT_COLOR, 'left',
                                self.FONT_NAME, self.font_size, False, False)
        self.main_text = Text(scene, self.geometry.top_left, '', self.MAIN_TEXT_COLOR, 'left', self.FONT_NAME,
                              self.font_size, False, False)

    def is_correct_symbol(self, symbol: str) -> bool:
        return symbol.isalnum()

    def set_main_str(self, new_main_str: str):
        self.main_str = new_main_str
        self.main_text.update_text(self.main_str)

    def process_logic(self):
        if self.controller.get_bumped_key():
            if self.controller.get_bumped_key() == pygame.K_BACKSPACE:
                self.set_main_str(self.main_str[0:-1])
            else:
                symbol = chr(self.controller.bumped_key)
                if self.is_correct_symbol(symbol):
                    self.set_main_str(self.main_str + symbol)

    def process_draw(self):
        pygame.draw.rect(self.scene.screen, self.BG_COLOR, rectangle_to_rect(self.geometry))
        if len(self.main_str) == 0:
            self.prompt_text.process_draw()
        else:
            self.main_text.process_draw()

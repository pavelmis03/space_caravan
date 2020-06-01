import pygame

from typing import Tuple

from scenes.base import Scene
from controller.controller import Controller
from drawable_objects.base import DrawableObject
from geometry.rectangle import tuple_to_rectangle, rectangle_to_rect
from geometry.point import Point
from drawable_objects.menu.text import Text
from utils.sound import SoundManager


class TextBox(DrawableObject):
    """
    Поле ввода пользователем строки. Сейчас принимает ввод всегда, когда его сцена работает. Поддерживает
    ввод маленьких латинских букв, цифр и пробела.

    :param scene: сцена объекта
    :param controller: контроллер
    :param geometry: кортеж c координатами прямоугольника поля ввода
    :param prompt_str: строка подсказки, показывающаяся, когда в поле ввода ничего не написано
    """
    PROMPT_TEXT_COLOR = (100, 100, 100)
    MAIN_TEXT_COLOR = (0, 0, 0)
    FONT_NAME = 'freesansbold'
    BG_COLOR = (255, 255, 255)
    TYPE_SOUND = 'ui.keytype'

    def __init__(self, scene: Scene, controller: Controller, geometry: Tuple, prompt_str: str):
        self.geometry = tuple_to_rectangle(geometry)
        super().__init__(scene, controller, self.geometry.center)
        font_size = round(self.geometry.height)
        self.prompt_str = prompt_str
        self.main_str = ''
        self.prompt_text = Text(scene, self.geometry.top_left, prompt_str, self.PROMPT_TEXT_COLOR, 'left',
                                self.FONT_NAME, font_size, False, False)
        self.main_text = Text(scene, self.geometry.top_left, '', self.MAIN_TEXT_COLOR, 'left', self.FONT_NAME,
                              font_size, False, False)

    def is_symbol_correct(self, symbol: str) -> bool:
        """
        Корректен ли введенный символ. Пока что поддерживается только маленьких латинских букв, цифр и пробела.
        """
        if 'a' <= symbol <= 'z':
            return True
        if '0' <= symbol <= '9':
            return True
        if symbol == ' ':
            return True
        return False

    @property
    def value(self) -> str:
        return self.main_str

    @value.setter
    def value(self, new_main_str: str):
        self.main_str = new_main_str
        self.main_text.update_text(self.main_str + '|')

    def move(self, movement: Point):
        """
        Перемещение объекта на заданный вектор. Необходимо для встраивания в WidgetGroup.
        """
        self.geometry.move(movement)
        self.main_text.pos += movement
        self.prompt_text.pos += movement

    def process_logic(self):
        """
        Логика объекта - фиксирование нажатий клавиш, воспринимаемых от контроллера.
        """
        if self.controller.get_bumped_key():
            SoundManager.play_sound(TextBox.TYPE_SOUND)
            if self.controller.get_bumped_key() == pygame.K_BACKSPACE:
                self.value = self.main_str[0:-1]
            else:
                symbol = chr(self.controller.bumped_key)
                if self.is_symbol_correct(symbol):
                    self.value = self.main_str + symbol

    def process_draw(self):
        pygame.draw.rect(self.scene.screen, self.BG_COLOR,
                         rectangle_to_rect(self.geometry))
        if len(self.main_str) == 0:
            self.prompt_text.process_draw()
        else:
            self.main_text.process_draw()

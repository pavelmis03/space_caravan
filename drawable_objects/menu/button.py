import pygame

from constants.color import COLOR
from drawable_objects.base import DrawableObject
from drawable_objects.menu.text import Text
from geometry.rectangle import rectangle_to_rect, tuple_to_rectangle
from utils.sound import SoundManager


class Button(DrawableObject):
    """
    Прямоугольная кнопка с текстом. При наведении на нее мыши меняет цвет. При нажании запускает заданную процедуру.

    :param scene: сцена, на которой кнопка находится
    :param controller: контроллер
    :param geometry: кортеж с координатами левого верхнего и правого нижнего углов кнопки
    :param text: текст
    :param function: процедура, которую кнопка исполнит по нажатию
    :param kwargs: именованные аргументы процедуры, вызываемой по нажатию
    :param font_size: размер шрифта текста на кнопке
    """
    BG_COLOR = (120, 120, 120)
    BG_HOVER_COLOR = (220, 220, 220)
    TEXT_COLOR = COLOR['BLACK']
    TEXT_HOVER_COLOR = COLOR['BLACK']
    FONT_NAME = 'zelekbold'
    HOVER_SOUND = 'ui.select'
    PRESS_SOUND = 'ui.press1'
    HOVER_RESIZE = 1.05

    def __init__(self, scene, controller, geometry, text='Test', function=None, kwargs=None, font_size=20):
        if not kwargs:
            kwargs = {}
        self.geometry = tuple_to_rectangle(geometry)
        super().__init__(scene, controller, self.geometry.center)
        self.function = function
        self.kwargs = kwargs
        self.hover = False
        self.text = Text(scene, self.geometry.center, text,
                         Button.TEXT_COLOR, 'center', Button.FONT_NAME, font_size)
        self.hover_text = Text(scene, self.geometry.center, text, Button.TEXT_HOVER_COLOR, 'center', Button.FONT_NAME,
                               font_size)
        SoundManager.set_volume(Button.HOVER_SOUND)
        # SoundManager.set_volume(Button.PRESS_SOUND)

    def move(self, movement):
        """
        Передвигает кнопку параллельным переносом на заданный вектор.

        :param movement: вектор переноса
        """
        self.geometry.move(movement)
        self.text.pos = self.geometry.center
        self.hover_text.pos = self.geometry.center

    def process_logic(self):
        hover = self.geometry.is_inside(self.controller.get_mouse_pos())
        if not self.hover and hover:
            SoundManager.play_sound(Button.HOVER_SOUND)
            self.geometry.width *= Button.HOVER_RESIZE
            self.geometry.height *= Button.HOVER_RESIZE
        elif self.hover and not hover:
            self.geometry.width /= Button.HOVER_RESIZE
            self.geometry.height /= Button.HOVER_RESIZE
        self.hover = hover
        click_pos = self.controller.get_click_pos()
        if click_pos and self.geometry.is_inside(click_pos):
            SoundManager.play_sound(Button.PRESS_SOUND)
            self.function(**self.kwargs)

    def process_draw(self):
        if self.hover:
            bg_color = Button.BG_HOVER_COLOR
            text = self.hover_text
        else:
            bg_color = Button.BG_COLOR
            text = self.text
        pygame.draw.rect(self.scene.screen, bg_color,
                         rectangle_to_rect(self.geometry))
        text.process_draw()

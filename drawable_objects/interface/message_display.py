"""
Модуль отвечающий за включение и выключение игровой паузы.
Так же заниемается отрисовкой меню во время паузы.
"""

import pygame

from constants.color import COLOR
from drawable_objects.base import AbstractObject
from drawable_objects.menu.multiline_text import MultilineText
from drawable_objects.menu.widget_group import WidgetGroup
from geometry.point import Point


class MessageDisplay(AbstractObject):
    """
    Класс, отвечающий за отображение внутриигровых сообщений
    CONTROLS - управление
    SURFACE_ALPHA - прозрачность фона cообщения
    SURFACE_COLOR - цвет фона сообщения
    """
    CONTROLS = {
        'CLOSE': pygame.K_RETURN
    }
    SURFACE_ALPHA = 160
    SURFACE_COLOR = COLOR['BLACK']

    def __init__(self, scene, controller, text):
        super().__init__(scene, controller)
        self.surface = pygame.Surface(
            (self.scene.game.width, self.scene.game.height))
        self.surface.set_alpha(MessageDisplay.SURFACE_ALPHA)
        self.surface.fill(MessageDisplay.SURFACE_COLOR)
        self.text = text

        """self.append(MultilineText(self.scene,Point (100,100),MessageDisplay.DESCRIPTION,
                                    color=COLOR['WHITE'], align='left',
                                    font_name='freesansbold', font_size=20,
                                    is_bold=False))"""
        self.buttons = WidgetGroup(self.scene, self.controller, [0.5, 0.3], 6)
        self.buttons.add_multilinetext(self.text,
                                    color=COLOR['WHITE'], align='center',
                                    font_name='freesansbold', font_size=20,
                                    is_bold=False)

        self.buttons.add_button('Закрыть', self.resume)

        self.active = False

    def process_logic(self):
        if self.controller.is_key_pressed(MessageDisplay.CONTROLS['CLOSE']) and self.active:
            self.resume()
        if self.active:
            self.surface = pygame.transform.scale(
                self.surface, (self.scene.game.width, self.scene.game.height))
            self.buttons.process_logic()

    def show(self):
        """
        Показ сообщения и приостановка игры
        """
        self.scene.game_paused_by += 1
        self.active = True

    def resume(self):
        """
        Отмена паузы игры и закрытие сообщения
        """
        self.scene.game_paused_by -= 1
        self.active = False
        self.scene.player.weapon.cooldown = 7

    def process_draw(self):
        if self.active:
            self.scene.screen.blit(self.surface, (0, 0))
            self.buttons.process_draw()

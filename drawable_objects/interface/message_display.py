"""
Модуль отвечающий за включение и выключение игровой паузы.
Так же заниемается отрисовкой меню во время паузы.
"""

import pygame

from constants.color import COLOR
from drawable_objects.base import AbstractObject
from drawable_objects.menu.widget_group import WidgetGroup


class MessageDisplay(AbstractObject):
    """
    Класс, отвечающий за отображение внутриигровых сообщений
    CONTROLS - управление
    SURFACE_ALPHA - прозрачность фона cообщения
    SURFACE_COLOR - цвет фона сообщения
    """
    CONTROLS = {
        'OPEN': pygame.K_ESCAPE,
        'CLOSE': pygame.K_RETURN
    }
    SURFACE_ALPHA = 160
    SURFACE_COLOR = COLOR['BLACK']

    def __init__(self, scene, controller):
        super().__init__(scene, controller)
        self.surface = pygame.Surface(
            (self.scene.game.width, self.scene.game.height))
        self.surface.set_alpha(MessageDisplay.SURFACE_ALPHA)
        self.surface.fill(MessageDisplay.SURFACE_COLOR)

        self.buttons = WidgetGroup(self.scene, self.controller, [0.5, 0.3], 6)
        self.buttons.add_button('Продолжить', self.resume)

        self.active = False

    def process_logic(self):
        if self.controller.is_key_pressed(MessageDisplay.CONTROLS['OPEN']) and not self.active:
            self.pause()
        if self.controller.is_key_pressed(MessageDisplay.CONTROLS['CLOSE']) and self.active:
            self.resume()
        if self.active:
            self.surface = pygame.transform.scale(
                self.surface, (self.scene.game.width, self.scene.game.height))
            self.buttons.process_logic()

    def pause(self):
        """
        Пауза игры
        """
        self.scene.game_paused = self.active = True

    def resume(self):
        """
        Отмена паузы игры
        """
        self.scene.game_paused = self.active = False
        self.scene.player.weapon.cooldown = 7

    def process_draw(self):
        if self.active:
            self.scene.screen.blit(self.surface, (0, 0))
            self.buttons.process_draw()

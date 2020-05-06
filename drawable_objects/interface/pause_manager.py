"""
Модуль отвечающий за включение и выключение игровой паузы.
Так же заниемается отрисовкой меню во время паузы.
"""

import pygame

from constants.color import COLOR
from drawable_objects.base import AbstractObject
from drawable_objects.interface.button_group import ButtonGroup


class PauseManager(AbstractObject):
    """
    Класс, отвечающий за паузу игры
    CONTROLS - управление
    SURFACE_ALPHA - прозрачность фона паузы
    SURFACE_COLOR - цвет фона паузы
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
        self.surface.set_alpha(PauseManager.SURFACE_ALPHA)
        self.surface.fill(PauseManager.SURFACE_COLOR)

        self.buttons = ButtonGroup(self.scene, self.controller, [
                                   0.5, 0.3], [150, 60], 6)
        self.buttons.add_button('Продолжить', self.resume)
        self.buttons.add_button('Главное меню', self.main_menu)

        self.active = False

    def process_logic(self):
        if self in self.controller.input_objects:
            if self.controller.is_key_pressed(PauseManager.CONTROLS['OPEN']) and not self.active:
                self.pause()
            if self.controller.is_key_pressed(PauseManager.CONTROLS['CLOSE']) and self.active:
                self.resume()
        if self.active:
            self.surface = pygame.transform.scale(self.surface, (self.scene.game.width, self.scene.game.height))
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

    def main_menu(self):
        """
        Переход в главное меню
        """
        self.resume()
        self.scene.game.toggle_scene(self.scene.game.MAIN_MENU_SCENE_INDEX)

    def process_draw(self):
        if self.active:
            self.scene.screen.blit(self.surface, (0, 0))
            self.buttons.process_draw()

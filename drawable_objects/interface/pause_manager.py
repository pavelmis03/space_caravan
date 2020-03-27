import pygame

from constants.color import Color
from drawable_objects.base import AbstractObject
from drawable_objects.button import Button


class PauseManager(AbstractObject):
    CONTROLS = {
        'OPEN': pygame.K_ESCAPE,
        'CLOSE': pygame.K_RETURN
    }
    SURFACE_ALPHA = 160
    SURFACE_COLOR = Color.BLACK

    def __init__(self, scene, controller):
        super().__init__(scene, controller)
        self.surface = pygame.Surface((self.scene.game.width, self.scene.game.height))
        self.surface.set_alpha(PauseManager.SURFACE_ALPHA)
        self.surface.fill(PauseManager.SURFACE_COLOR)

        self.buttons = [
            Button(self.scene, self.controller, (350, 155, 450, 195), 'Продолжить', self.unpause),
            Button(self.scene, self.controller, (350, 205, 450, 245), 'Главное меню', self.main_menu),
        ]
        self.active = False

    def process_logic(self):
        if self in self.controller.input_objects:
            if self.controller.is_key_pressed(PauseManager.CONTROLS['OPEN']) and not self.active:
                self.pause()
            if self.controller.is_key_pressed(PauseManager.CONTROLS['CLOSE']) and self.active:
                self.unpause()
        if self.active:
            for button in self.buttons:
                button.process_logic()

    def pause(self):
        self.scene.game_paused = self.active = True

    def unpause(self):
        self.scene.game_paused = self.active = False

    def main_menu(self):
        self.unpause()
        self.scene.game.set_scene(self.scene.game.MAIN_MENU_SCENE_INDEX)

    def process_draw(self):
        if self.active:
            self.scene.screen.blit(self.surface, (0, 0))
            for button in self.buttons:
                button.process_draw()
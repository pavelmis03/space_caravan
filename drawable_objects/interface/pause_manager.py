import pygame

from constants import Color
from drawable_objects.base import AbstractObject


class PauseManager(AbstractObject):
    OPEN = pygame.K_ESCAPE
    SURFACE_ALPHA = 160
    SURFACE_COLOR = Color.BLACK

    def __init__(self, scene, controller):
        super().__init__(scene, controller)
        self.surface = pygame.Surface((self.scene.game.width, self.scene.game.height))
        self.surface.set_alpha(PauseManager.SURFACE_ALPHA)
        self.surface.fill(PauseManager.SURFACE_COLOR)

        self.buttons = []
        self.active = False

    def process_logic(self):
        if self in self.controller.input_objects:
            if self.controller.is_key_pressed(PauseManager.OPEN):
                self.scene.game_paused = self.active = True

    def process_draw(self):
        if self.active:
            self.scene.screen.blit(self.surface, (0, 0))
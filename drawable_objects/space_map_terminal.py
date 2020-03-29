import math

import pygame

from drawable_objects.base import GameSprite
from geometry.point import Point
from geometry.distances import dist

from scenes.base import Scene
from controller.controller import Controller

class SpaceMapTerminal(GameSprite):

    IMAGE_ZOOM = 0.3

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__ (scene, controller, 'player', pos, angle, SpaceMapTerminal.IMAGE_ZOOM)


    def process_logic(self):
        if dist(self.pos, self.scene.player.pos) <= 100:
            if self.controller.is_key_pressed(key=pygame.K_e):
                self.scene.game.set_scene(1)


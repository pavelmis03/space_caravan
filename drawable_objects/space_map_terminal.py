from drawable_objects.base import UsableObject
from geometry.point import Point

from scenes.base import Scene
from controller.controller import Controller

from drawable_objects.player import Player

class SpaceMapTerminal(UsableObject):

    IMAGE_ZOOM = 0.3

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__ (scene, controller, Player.IMAGE_NAME, pos, angle, SpaceMapTerminal.IMAGE_ZOOM)

    def activate(self):
        self.scene.game.set_scene(self.scene.game.SPACEMAP_SCENE_INDEX)

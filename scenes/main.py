from constants import Color
from drawable_objects.player import Player
from scenes.base import Scene
from geometry.basic_geometry import Point

class MainScene(Scene):

    def create_objects(self):
        self.player = Player(self, None, Point(400, 400), 0)
        self.objects = [self.player]

    def additional_logic(self):
        # self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)
        pass
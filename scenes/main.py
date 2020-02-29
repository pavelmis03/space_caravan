from constants import Color
from drawable_objects.player import Player
from scenes.base import Scene


class MainScene(Scene):

    def create_objects(self):
        self.player = Player(self.game)
        self.objects = [self.player]

    def additional_logic(self):
        # self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)
        pass
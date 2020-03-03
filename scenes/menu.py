from drawable_objects.button import Button
from scenes.base import Scene


class MenuScene(Scene):
    def create_objects(self):
        self.interface_objects.append(Button(self, self.game.controller, (350, 255, 450, 295), 'Играть',
                                             self.game.set_scene, { 'scene_index': self.game.MAIN_SCENE_INDEX }))
        self.interface_objects.append(Button(self, self.game.controller, (350, 305, 450, 345), 'Выход', self.game.end))

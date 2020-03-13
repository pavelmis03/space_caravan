from drawable_objects.button import Button
from scenes.base import Scene


class MenuScene(Scene):
    """
    Сцена главной страницы меню.

    :param game: игра, создающая сцену
    """
    def __init__(self, game):
        super().__init__(game)
        self.interface_objects.append(Button(self, self.game.controller, (350, 255, 450, 295), 'Играть',
                                             self.game.set_scene, { 'scene_index': self.game.MAIN_SCENE_INDEX }))
        self.interface_objects.append(Button(self, self.game.controller, (350, 305, 450, 345), 'Выход', self.game.end))

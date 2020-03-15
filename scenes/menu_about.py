from drawable_objects.button import Button
from scenes.menu import MenuScene


class About_MenuScene(MenuScene):
    """
    Сцена главной страницы меню.

    :param game: игра, создающая сцену
    """
    def __init__(self, game):
        super().__init__(game)
        self.interface_objects.append(Button(self, self.game.controller, (350, 305, 450, 345), 'Назад',
                                             self.game.set_scene, {'scene_index': self.game.MAIN_MENU_SCENE_INDEX}))
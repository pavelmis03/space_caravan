from scenes.game.base import GameScene
from scenes.menu.base import MenuScene


class SettingsMenuScene(MenuScene):
    """
    Сцена страницы настроек меню.

    :param game: игра, создающая сцену
    """

    def __init__(self, game):
        super().__init__(game)
        self.menu.add_checkbox('Фиксированная камера')
        self.menu.add_button('Назад', self.button_back)

    def button_back(self):
        GameScene.FIXED_CAMERA = self.menu.widgets[0].check
        self.game.set_scene_with_index(self.game.MAIN_MENU_SCENE_INDEX)

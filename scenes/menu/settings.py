"""
Класс страницы настроек меню
"""
from scenes.menu.base import MenuScene


class SettingsMenuScene(MenuScene):
    """
    Сцена страницы настроек меню.

    :param game: игра, создающая сцену
    """

    def __init__(self, game):
        super().__init__(game)
        self.menu.add_button('Назад', self.game.set_scene_with_index, {
                             'scene_index': self.game.MAIN_MENU_SCENE_INDEX})

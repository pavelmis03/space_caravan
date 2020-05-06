"""
Класс главной страницы меню меню
"""

from scenes.menu.base import MenuScene


class MainMenuScene(MenuScene):
    """
    Сцена главной страницы меню.

    :param game: игра, создающая сцену
    """

    def __init__(self, game):
        super().__init__(game)

        self.menu.add_button('Играть', self.game.toggle_scene, {
                             'scene_index': self.game.SPACESHIP_SCENE_INDEX})
        self.menu.add_button('Настройки', self.game.toggle_scene, {
                             'scene_index': self.game.SETTINGS_MENU_SCENE_INDEX})
        self.menu.add_button('О нас', self.game.toggle_scene, {
                             'scene_index': self.game.ABOUT_MENU_SCENE_INDEX})
        self.menu.add_button('Выход', self.game.end)

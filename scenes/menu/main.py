"""
Класс главной страницы меню меню
"""
from geometry.point import Point
from scenes.menu.base import MenuScene


class MainMenuScene(MenuScene):
    """
    Сцена главной страницы меню.

    :param game: игра, создающая сцену
    """

    def __init__(self, game):
        super().__init__(game)
        self.menu.update_offset([0.5, 0.2])
        self.menu.add_multilinetext('Space Caravan', align='center',
                                    font_name='zelekbold', font_size=90)

        self.menu.add_button('Играть', self.game.set_scene_with_index, {
            'scene_index': self.game.SPACE_CHOICE_MENU_SCENE_INDEX
        })
        self.menu.add_button('Настройки', self.game.set_scene_with_index, {
                             'scene_index': self.game.SETTINGS_MENU_SCENE_INDEX})
        self.menu.add_button('О нас', self.game.set_scene_with_index, {
                             'scene_index': self.game.ABOUT_MENU_SCENE_INDEX})
        self.menu.add_button('Выход', self.game.end)

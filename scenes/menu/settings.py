"""
Класс страницы настроек меню
"""
from drawable_objects.checkbox import CheckBox
from scenes.menu.base import MenuScene


class SettingsMenuScene(MenuScene):
    """
    Сцена страницы настроек меню.

    :param game: игра, создающая сцену
    """

    def __init__(self, game):
        super().__init__(game)
        test_check = CheckBox(self, self.game.controller, (200, 200, 300, 300),
                              'Подвижная камера', enabled=True)
        self.interface_objects.append(test_check)
        self.menu.add_button('Назад', self.game.set_scene, {
                             'scene_index': self.game.MAIN_MENU_SCENE_INDEX})

from typing import Dict

from scenes.game.level import LevelScene
from scenes.menu.base import MenuScene


class SettingsMenuScene(MenuScene):
    """
    Сцена страницы настроек меню.

    :param game: игра, создающая сцену
    """
    DATA_FILENAME = 'settings'

    def __init__(self, game):
        super().__init__(game)
        self.fixed_camera_checkbox = self.menu.add_checkbox('Фиксированная камера')
        self.menu.add_button('Назад', self.button_back)

    def button_back(self):
        LevelScene.FIXED_CAMERA = self.menu.widgets[0].check
        self.game.set_scene_with_index(self.game.MAIN_MENU_SCENE_INDEX)

    def from_dict(self, data_dict: Dict):
        super().from_dict(data_dict)
        self.fixed_camera_checkbox.from_dict(data_dict['fixed_camera_checkbox'])

    def to_dict(self) -> Dict:
        result = super().to_dict()
        result.update({
            'fixed_camera_checkbox': self.fixed_camera_checkbox.to_dict(),
        })
        return result

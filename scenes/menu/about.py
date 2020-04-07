from constants.color import Color
from drawable_objects.text import Text
from geometry.point import Point
from scenes.menu.base import MenuScene


class About_MenuScene(MenuScene):
    """
    Сцена "О нас" главной страницы меню

    :param game: игра, создающая сцену
    """
    DESCRIPTION = """[IN DEVELOPMENT]"""

    def __init__(self, game):
        super().__init__(game)
        self.menu.update_offset([0.5, 0.5])
        x, y = self.menu.pos
        label = Text(self, Point(x, y-100), About_MenuScene.DESCRIPTION, Color.WHITE, 'center', 'Consolas', 20)
        self.interface_objects.append(label)
        self.menu.add_button('Назад', self.game.set_scene, {'scene_index': self.game.MAIN_MENU_SCENE_INDEX})
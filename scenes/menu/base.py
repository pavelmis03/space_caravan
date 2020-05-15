"""
Основа для создания сцен меню
"""

from drawable_objects.interface.widget_group import WidgetGroup
from scenes.base import Scene


class MenuScene(Scene):
    """
    Базовый класс для сцены меню

    :param game: игра, создающая сцену
    """

    def __init__(self, game):
        super().__init__(game)
        self.menu = WidgetGroup(self, self.game.controller, [0.5, 0.3], 6)
        self.interface_objects.append(self.menu)

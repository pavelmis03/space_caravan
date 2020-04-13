from drawable_objects.interface.button_group import ButtonGroup
from scenes.base import Scene


class MenuScene(Scene):
    """
    Базовый класс для сцены меню

    :param game: игра, создающая сцену
    """

    def __init__(self, game):
        super().__init__(game)
        self.menu = ButtonGroup(self, self.game.controller, [
                                0.5, 0.3], [150, 60], 6)
        self.interface_objects.append(self.menu)

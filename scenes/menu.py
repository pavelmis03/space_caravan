from drawable_objects.button import Button
from scenes.base import Scene


class MenuScene(Scene):
    """
    Сцена главной страницы меню.

    :param game: игра, создающая сцену
    """
    def __init__(self, game):
        super().__init__(game)
        self.interface_objects.append(Button(self, self.game.controller, (350, 355, 450, 395), 'Выход', self.game.end))

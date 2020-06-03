from scenes.menu.redirecting.base import RedirectingScene
from constants.color import COLOR


class VictoryScene(RedirectingScene):
    """
    Сцена победы в игре. Перенаправляет на сцену космического корабля.
    """

    DESCRIPTION = '''
    Вы победили всех врагов!
    Поздравляем, игра пройдена!
    '''
    TEXT_COLOR = COLOR['LIGHT_GREEN']
    FONT_SIZE = 70

    def __init__(self, game):
        super().__init__(game)

    def redirect(self):
        from scenes.game.spaceship import SpaceshipScene
        spaceship_scene = SpaceshipScene(self.game)
        self.game.set_scene(spaceship_scene)

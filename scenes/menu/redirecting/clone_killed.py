from scenes.menu.redirecting.base import RedirectingScene


class CloneKilledScene(RedirectingScene):
    """
    Сцена с сообщением об убийстве клона. Перенаправляет на сцену космического корабля.
    """
    DESCRIPTION = '''
    Клон убит.
    Высадка провалена.
    '''

    def __init__(self, game):
        super().__init__(game)

    def redirect(self):
        from scenes.game.spaceship import SpaceshipScene
        spaceship_scene = SpaceshipScene(self.game)
        self.game.set_scene(spaceship_scene)

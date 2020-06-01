from scenes.menu.redirecting.base import RedirectingScene


class GameoverScene(RedirectingScene):
    """
    Сцена конца игры. Перенаправляет на главную сцену меню.
    """

    DESCRIPTION = '''
    Вы были убиты.
    Игра окончена!
    '''

    def __init__(self, game):
        super().__init__(game)

    def redirect(self):
        self.game.set_scene_with_index(self.game.MAIN_MENU_SCENE_INDEX)

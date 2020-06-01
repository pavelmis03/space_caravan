"""
Класс странички "О нас" меню
"""

from constants.color import COLOR
from scenes.menu.base import MenuScene


class AboutMenuScene(MenuScene):
    """
    Сцена "О нас" главной страницы меню

    :param game: игра, создающая сцену
    """
    DESCRIPTION = """
        Мы - ребята из школы программистов, 
        группа 104, промышленное программирование.
        Мы очень любим программировать, особенно на питоне.
        Данный проект разрабатывался нами очень долго и дался большой ценой.
        Это наш последний проект вместе как учеников, но возможно мы еще соберемся в будущем.
        Наслаждайтесь процессом игры!
        Сорочан Илья, Бахарев Никита, Пономарев Андрей,
        Гулинкин Михаил, Кильдишев Петр, Кильдишев Александр
        Дизайнер: Емельянова Татьяна
    """

    def __init__(self, game):
        super().__init__(game)
        self.menu.add_multilinetext(AboutMenuScene.DESCRIPTION,
                                    color=COLOR['WHITE'], align='center',
                                    font_name='freesansbold', font_size=20,
                                    is_bold=False)
        self.menu.add_button('Назад', self.game.set_scene_with_index,
                             {'scene_index': self.game.MAIN_MENU_SCENE_INDEX})

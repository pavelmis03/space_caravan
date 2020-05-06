"""
Класс странички "О нас" меню
"""

from constants.color import COLOR
from drawable_objects.multiline_text import MultilineText
from geometry.point import Point
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
    """

    def __init__(self, game):
        super().__init__(game)
        self.menu.update_offset([0.5, 0.5])
        x, y = self.menu.pos
        label = MultilineText(self, Point(x, y-200), AboutMenuScene.DESCRIPTION,
                              COLOR['WHITE'], 'center', 'Consolas', 20)
        self.interface_objects.append(label)
        self.menu.add_button('Назад', self.game.toggle_scene,
                             {'scene_index': self.game.MAIN_MENU_SCENE_INDEX})

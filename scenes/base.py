import pygame

from constants.color import COLOR
from geometry.point import Point

class Scene:
    """
    Базовый класс сцены.

    :param game: игра, создающая сцену
    """

    CLEAR_COLOR = COLOR['BLACK']

    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.interface_objects = []

    @property
    def width(self):
        return self.game.width

    @property
    def height(self):
        return self.game.height

    @property
    def center(self):
        return Point(self.width / 2, self.height / 2)

    def iteration(self):
        """
        Итерация работы сцены - обработка логики и отрисовка. Далее команда двойной буферизации и задержка
        между тактами.
        """
        self.process_all_logic()
        self.process_all_draw()
        pygame.display.flip()
        pygame.time.wait(10)

    def interface_logic(self):
        for item in self.interface_objects:
            item.process_logic()

    def process_all_logic(self):
        """
        Логика сцены и ее объектов.
        """
        self.interface_logic()

    def clear_screen(self):
        self.screen.fill(self.CLEAR_COLOR)

    def interface_draw(self):
        for item in self.interface_objects:
            item.process_draw()

    def process_all_draw(self):
        """
        Отрисовка сцены и ее объектов.
        """
        self.clear_screen()
        self.interface_draw()

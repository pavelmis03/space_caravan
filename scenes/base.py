import pygame

from constants import Color
from geometry.point import Point


class Scene:
    """
    Базовый класс сцены.

    :param game: игра, создающая сцену
    """
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.interface_objects = []

    def iteration(self):
        self.process_all_logic()
        self.process_all_draw()
        pygame.display.flip()  # double buffering
        pygame.time.wait(10)  # подождать 10 миллисекунд

    def process_all_logic(self):
        for item in self.interface_objects:
            item.process_logic()

    def process_all_draw(self):
        self.screen.fill(Color.BLACK)
        for item in self.interface_objects:
            item.process_draw()


class GameScene(Scene):
    """
    Класс игровой сцены, где помимо объектов интерфейса есть игровые объекты, игрок и сетка.

    :param game: игра, создающая сцену
    """
    def __init__(self, game):
        super().__init__(game)
        self.game_objects = []
        self.relative_center = Point(0, 0)
        self.grid = None
        self.player = None

    def process_all_logic(self):
        """
        Обработка логики в следующем порядке: объекты интерфейса, сетка, игровые объекты, игрок.
        """
        for item in self.interface_objects:
            item.process_logic()
        self.grid.process_logic()
        for item in self.game_objects:
            item.process_logic()
        self.player.process_logic()
        self.relative_center = self.player.pos - self.game.screen_rectangle.center

    def process_all_draw(self):
        """
        Отрисовка в следующем порядке: сетка, игровые объекты, игрок, объекты интерфейса.
        """
        self.screen.fill(Color.BLACK)
        self.grid.process_draw()
        for item in self.game_objects:
            item.process_draw()
        self.player.process_draw()
        for item in self.interface_objects:
            item.process_draw()

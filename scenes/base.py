import pygame

from constants.color import Color
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
        Итерация работы сцены - обработка логики и отрисовка.
        """
        self.process_all_logic()
        self.process_all_draw()
        pygame.display.flip()  # double buffering
        pygame.time.wait(10)  # подождать 10 миллисекунд

    def process_all_logic(self):
        """
        Обработка логики сцены и ее объектов.
        """
        for item in self.interface_objects:
            item.process_logic()

    def process_all_draw(self):
        """
        Обработка отрисовки сцены и ее объектов.
        """
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
        self.plane = None
        self.game_paused = False
        self.delete_me_later = []

    def process_all_logic(self):
        """
        Обработка логики в следующем порядке: объекты интерфейса, сетка, игровые объекты, игрок.
        Если флаг game_paused установлен в True, то логика вызывается только для объектов интерфейса
        """
        for item in self.interface_objects:
            item.process_logic()
        if not self.game_paused:
            self.grid.process_logic()
            for item in self.game_objects:
                item.process_logic()
            self.player.process_logic()
            self.relative_center = self.player.pos - self.game.screen_rectangle.center
            self.relative_center = self.grid.get_correct_relative_pos(self.relative_center)
        # Удаление уничтоженных игровых объектов
        for item in self.game_objects:
            if not item.enabled:
                self.game_objects.remove(item)

    def process_all_draw(self):
        """
        Отрисовка в следующем порядке: сетка, игровые объекты, игрок, объекты интерфейса.
        """
        self.screen.fill(Color.BLACK)
        self.grid.process_draw()
        for i in range(len(self.delete_me_later)):
            self.delete_me_later[i].process_draw()
        for item in self.game_objects:
            item.process_draw()
        self.player.process_draw()
        for item in self.interface_objects:
            item.process_draw()

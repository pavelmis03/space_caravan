import string

#MVC


#MODEL
import pygame

from drawable_objects.base import DrawableObject


class ConsoleModel:
    pass


#VIEWER
class Console(DrawableObject):
    INPUTDICT = string.ascii_letters + string.digits
    CONTROLS = pygame.K_RETURN
    PRESS_DELAY = 6

    def __init__(self, scene, controller, pos):
        super().__init__(scene, controller, pos)
        self.presscnt = 1
        self.console_status = False

    def process_logic(self):
        if self in self.controller.input_objects:
            for ch in Console.INPUTDICT:
                if self.controller.is_key_pressed(ord(ch)):
                    print(ch, end=' ')
            print()
        if self.controller.is_key_pressed(Console.CONTROLS):
            self.presscnt += 1
            self.presscnt %= Console.PRESS_DELAY

        if self.presscnt == 0:
            print('Console', self.console_status)
            self.console_status = not self.console_status
            self.presscnt += 1

    def process_draw(self, relative_center):
        """
        Отрисовка объекта в относительных координатах

        :param relative_center: центр относительных координат
        """
        pass


#CONTROLLER
class ConsoleController:
    pass
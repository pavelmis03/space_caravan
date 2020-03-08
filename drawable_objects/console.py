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

    def __init__(self, scene, controller, pos):
        super().__init__(scene, controller, pos)

    def process_logic(self):
        if self in self.controller.input_objects:
            for ch in Console.INPUTDICT:
                if self.controller.is_key_pressed(ord(ch)):
                    print(ch, end=' ')
            print()
        if self.controller.is_key_pressed(Console.CONTROLS):
            print('Console')

    def process_draw(self, rel):
        pass # заглушка


#CONTROLLER
class ConsoleController:
    pass
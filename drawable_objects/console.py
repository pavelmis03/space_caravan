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
    CONTROLS = {
        'on': [pygame.K_SLASH],
        'off': [pygame.K_ESCAPE, pygame.K_RETURN],
    }

    def __init__(self, scene, controller, pos):
        super().__init__(scene, controller, pos)
        self.presscnt = 1
        self.console_on = False

    def process_logic(self):
        if self in self.controller.input_objects:
            for ch in Console.INPUTDICT:
                if self.controller.is_key_pressed(ord(ch)):
                    print(ch, end=' ')
            print()
        if self.controller.is_one_of_keys_pressed(Console.CONTROLS['on']):
            print('Console is now on')
            self.switch_on()
        if self.controller.is_one_of_keys_pressed(Console.CONTROLS['off']):
            print('Console is now off')
            self.switch_off()

    def switch_on(self):
        self.console_on = True
        self.controller.input_objects = [self]

    def switch_off(self):
        self.console_on = False
        self.controller.input_objects = [self.scene.player]


    def process_draw(self):
        """
        Отрисовка объекта в относительных координатах

        :param relative_center: центр относительных координат
        """
        relative_center = self.scene.relative_center
        relative_pos = self.pos - relative_center


#CONTROLLER
class ConsoleController:
    pass
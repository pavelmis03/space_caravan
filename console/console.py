import string
import pygame

from drawable_objects.base import DrawableObject

#MVC
# Viewer will display console
# Controller would be getting keys when Viewer is active
# Model will parse and run commands, which controller got


#MODEL
class ConsoleModel:
    pass


#VIEWER
class Console(DrawableObject):
    CONTROLS = {
        'on': [pygame.K_SLASH],
        'off': [pygame.K_ESCAPE, pygame.K_RETURN],
    }

    def __init__(self, scene, controller, pos):
        super().__init__(scene, controller, pos)
        self.console_on = False
        self.console_controller = ConsoleController(scene, controller, self)

    def process_logic(self):
        # change text on lable

        if self.controller.is_one_of_keys_pressed(Console.CONTROLS['on']):
            print('Console is now on')
            self.switch(True)
        if self.controller.is_one_of_keys_pressed(Console.CONTROLS['off']):
            print('Console is now off')
            self.switch(False)

        self.console_controller.process_logic()

    def process_draw(self):
        relative_center = self.scene.relative_center
        relative_pos = self.pos - relative_center
        pass

    def switch(self, state):
        self.console_on = state
        if state:
            self.controller.input_objects = [self]
        else:
            self.controller.input_objects = [self.scene.player]


#CONTROLLER
class ConsoleController:
    INPUTDICT = string.ascii_letters + string.digits

    def __init__(self, scene, controller, console):
        self.scene = scene
        self.controller = controller
        self.console = console
        self.text = ""

    def process_logic(self):
        if self.console.console_on:
            for ch in ConsoleController.INPUTDICT:
                if self.controller.is_key_pressed(ord(ch)):
                    self.text += ch
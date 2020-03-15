import string
import pygame

from console.entry import Entry
from drawable_objects.base import AbstractObject


class Console(AbstractObject):
    CONTROLS = {
        'on': [pygame.K_SLASH],
        'off': [pygame.K_RETURN, pygame.K_ESCAPE],  # first to enter, second to exit
    }

    def __init__(self, scene, controller, entry_rect):
        super().__init__(scene, controller)
        self.console_entry = Entry(scene, controller, entry_rect, initial_text="/", visible=False)
        self.console_controller = ConsoleController(scene, controller)
        self.console_controller.clear()

    def process_logic(self):
        self.console_controller.process_logic()
        self.update_text()

        if self.controller.is_one_of_keys_pressed(self.CONTROLS['on']):
            print('Console on')
            self.console_on()
        if self.controller.is_one_of_keys_pressed(self.CONTROLS['off']):
            print('Console off')
            self.console_off()

    def console_on(self):
        self.controller.input_objects = [self.console_controller]
        self.console_entry.show()

    def console_off(self):
        self.controller.input_objects = [self.scene.player]
        self.console_entry.hide()
        # TODO here's check on enter or escape and command run
        cmd = self.console_controller.text
        print("Attempting to run command '{}'".format(cmd))
        self.console_controller.clear()

    def process_draw(self):
        self.console_entry.process_draw()

    def update_text(self):
        self.console_entry.text.update_text(self.console_controller.text)


class ConsoleController(AbstractObject):
    INPUTDICT = string.ascii_letters + string.digits

    def __init__(self, scene, controller):
        super().__init__(scene, controller)
        self.text = ""

    def process_logic(self):
        if self in self.controller.input_objects:
            for ch in ConsoleController.INPUTDICT:
                if self.controller.is_key_pressed(ord(ch)):
                    self.text += ch

    def clear(self):
        self.text = "/"
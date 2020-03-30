"""
Неиспользуемый модуль. Может, позже пригодится.
"""
import string
import pygame

from console.entry import Entry
from drawable_objects.base import AbstractObject


class Console(AbstractObject):
    ENTRY_WIDTH_LIMIT=190

    def __init__(self, scene, controller, entry_rect):
        super().__init__(scene, controller)
        self.console_entry = Entry(scene, controller, entry_rect, initial_text="/", visible=False, width_limit=Console.ENTRY_WIDTH_LIMIT)
        self.console_controller = ConsoleController(scene, controller)
        self.console_controller.clear()

    def process_logic(self):
        self.console_controller.process_logic()
        self.update_text()

        if self.console_controller.is_on_pressed():
            print('Console on')
            self.console_on()
        if self.console_controller.is_off_pressed():
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
    INPUTDICT = string.ascii_letters + string.digits + " "
    CONTROLS = {
        'on': [pygame.K_SLASH],
        'off': [pygame.K_RETURN, pygame.K_ESCAPE],  # first to enter, second to exit
        'erase': [pygame.K_BACKSPACE]
    }

    def __init__(self, scene, controller):
        super().__init__(scene, controller)
        self.text = ""
        self.key_down = []

    def process_logic(self):
        if self in self.controller.input_objects:
            pressed = list(map(chr, self.controller.pressed_keys))
            for ch in pressed:
                if ch in ConsoleController.INPUTDICT and ch not in self.key_down:
                    self.text += ch
                if ord(ch) in ConsoleController.CONTROLS['erase'] and ch not in self.key_down:
                    self.text = self.text[:-1]
            self.key_down = pressed

    def is_on_pressed(self):
        return self.controller.is_one_of_keys_pressed(ConsoleController.CONTROLS['on'])

    def is_off_pressed(self):
        return self.controller.is_one_of_keys_pressed(ConsoleController.CONTROLS['off'])

    def clear(self):
        self.text = "/"
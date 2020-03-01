import pygame

from geometry.point import Point, tuple_to_point


class Controller:
    def __init__(self, game):
        self.game = game

        self.mouse_pos = Point()
        self.click_pos = None
        self.click_button = None
        self.pressed_keys = set()

    def iteration(self):
        self.click_pos = self.click_button = None
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                print('Пользователь нажал крестик')
                self.game.end()
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = tuple_to_point(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click_pos = tuple_to_point(event.pos)
                self.click_button = event.button
            elif event.type == pygame.KEYDOWN:
                if event.key not in self.pressed_keys:
                    self.pressed_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self.pressed_keys:
                    self.pressed_keys.remove(event.key)

    def get_mouse_pos(self):
        return self.mouse_pos

    def get_click_pos(self):
        return self.click_pos

    def get_click_button(self):
        return self.click_button

    def is_key_pressed(self, key):
        return key in self.pressed_keys

from scenes.menu.base import MenuScene
from drawable_objects.textbox import TextBox
from drawable_objects.list_widget import ListWidget
from drawable_objects.button import Button
from scenes.game.spaceship import SpaceshipScene


class SpaceChoiceMenuScene(MenuScene):
    def __init__(self, game):
        super().__init__(game)
        self.space_name_textbox = TextBox(
            self, self.game.controller, (100, 400, 900, 450), "new space name")
        self.space_names_list_widget = ListWidget(self, self.game.controller, (100, 50, 900, 350), 50,
                                                  self.game.file_manager.get_all_space_names())
        new_space_button = Button(self, self.game.controller, (100, 500, 350, 600), "Создать космос",
                                  self.create_space)
        delete_space_button = Button(self, self.game.controller, (375, 500, 625, 600), "Удалить космос",
                                     self.delete_space)
        start_game_button = Button(self, self.game.controller, (650, 500, 900, 600), "Начать игру",
                                   self.start_game)

        self.interface_objects.append(new_space_button)
        self.interface_objects.append(delete_space_button)
        self.interface_objects.append(start_game_button)
        self.interface_objects.append(self.space_name_textbox)
        self.interface_objects.append(self.space_names_list_widget)

    def create_space(self):
        space_name = self.space_name_textbox.value
        if space_name == '' or space_name in self.space_names_list_widget:
            return
        self.space_name_textbox.value = ''
        self.game.file_manager.set_current_space(space_name)
        self.game.file_manager.create_space_storage()
        self.space_names_list_widget.add_element(space_name)
        spaceship_scene = SpaceshipScene(self.game)
        spaceship_scene.initialize()
        spaceship_scene.save()

    def delete_space(self):
        space_name = self.space_names_list_widget.choice
        if not space_name:
            return
        self.space_names_list_widget.remove_element(space_name)
        self.game.file_manager.set_current_space(space_name)
        self.game.file_manager.delete_space_storage()

    def start_game(self):
        space_name = self.space_names_list_widget.choice
        if not space_name:
            return
        self.game.file_manager.set_current_space(space_name)
        spaceship_scene = SpaceshipScene(self.game)
        spaceship_scene.load()
        self.game.set_scene(spaceship_scene)

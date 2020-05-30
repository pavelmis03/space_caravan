from scenes.menu.base import MenuScene
from drawable_objects.textbox import TextBox
from drawable_objects.list_widget import ListWidget
from drawable_objects.button import Button
from scenes.game.spaceship import SpaceshipScene


class SpaceChoiceMenuScene(MenuScene):
    """
    Сцена выбора космоса для игры. Также позволяет управлять игровыми мирами: создавать и удалять.
    """
    def __init__(self, game):
        super().__init__(game)
        self.space_names_list_widget = ListWidget(self, self.game.controller, (100, 25, 900, 325), 50,
                                                  self.game.file_manager.get_all_space_names())
        self.space_name_textbox = TextBox(self, self.game.controller, (100, 350, 900, 400), "new space name")
        new_space_button = Button(self, self.game.controller, (100, 425, 350, 525), "Создать космос",
                                  self.create_space)
        delete_space_button = Button(self, self.game.controller, (375, 425, 625, 525), "Удалить космос",
                                     self.delete_space)
        start_game_button = Button(self, self.game.controller, (650, 425, 900, 525), "Начать игру",
                                   self.start_game)
        back_button = Button(self, self.game.controller, (375, 550, 625, 650), "Назад", self.game.set_scene_with_index,
                             {'scene_index': self.game.MAIN_MENU_SCENE_INDEX})

        self.interface_objects.append(new_space_button)
        self.interface_objects.append(delete_space_button)
        self.interface_objects.append(start_game_button)
        self.interface_objects.append(back_button)
        self.interface_objects.append(self.space_name_textbox)
        self.interface_objects.append(self.space_names_list_widget)

    def init_spaceship_scene(self):
        """
        Инициализация сцены космического корабля, которая включает в себя создание игрока. Проинициализированная
        сцена и игрок сохраняются и выбрасываются. При последующих загрузках космоса будет происходить загрузка из
        файлов.
        """
        spaceship_scene = SpaceshipScene(self.game)
        spaceship_scene.construct()

    def create_space(self):
        """
        Создание нового космоса: очистка поля ввода, добавление пункта в список для пользователя, создание
        хранилища файлов, инициализация игрового мира. Если поле ввода пустое или космос с введенным
        именем уже есть, ничего не происходит.
        """
        space_name = self.space_name_textbox.value
        if space_name == '' or space_name in self.space_names_list_widget:
            return
        self.space_name_textbox.value = ''
        self.game.file_manager.set_current_space(space_name)
        self.game.file_manager.create_space_storage()
        self.space_names_list_widget.add_element(space_name)
        self.init_spaceship_scene()

    def delete_space(self):
        """
        Удаление космоса. Удаляется пункт пользовательского списка и хранилище файлов. Если космос не выбран,
        ничего не происходит.
        """
        space_name = self.space_names_list_widget.choice
        if not space_name:
            return
        self.space_names_list_widget.remove_element(space_name)
        self.game.file_manager.set_current_space(space_name)
        self.game.file_manager.delete_space_storage()

    def start_game(self):
        """
        Старт игры в выбранном пользователем космосе. Загружается и отображается сцена космического корабля. Если
        космос не выбран, ничего не происходит.
        """
        space_name = self.space_names_list_widget.choice
        if not space_name:
            return
        self.game.file_manager.set_current_space(space_name)
        spaceship_scene = SpaceshipScene(self.game)
        self.game.set_scene(spaceship_scene)

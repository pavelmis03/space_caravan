from drawable_objects.button import Button
from scenes.menu import MenuScene


class Main_MenuScene(MenuScene):
    """
    Сцена главной страницы меню.

    :param game: игра, создающая сцену
    """
    def __init__(self, game):
        super().__init__(game)
        self.interface_objects.append(Button(self, self.game.controller, (350, 155, 450, 195), 'Играть',
                                             self.game.set_scene, { 'scene_index': self.game.SPACEMAP_SCENE_INDEX }))
        self.interface_objects.append(Button(self, self.game.controller, (350, 205, 450, 245), 'Настройки',
                                             self.game.set_scene, { 'scene_index': self.game.SETTINGS_MENU_SCENE_INDEX }))
        self.interface_objects.append(Button(self, self.game.controller, (350, 255, 450, 295), 'О нас',
                                             self.game.set_scene, { 'scene_index': self.game.ABOUT_MENU_SCENE_INDEX }))


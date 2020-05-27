from scenes.menu.base import MenuScene
from drawable_objects.textbox import TextBox


class WorldChoiceMenuScene(MenuScene):
    def __init__(self, game):
        super().__init__(game)
        self.interface_objects.append(TextBox(self, self.game.controller, (100, 100, 500, 150), "Enter text!"))

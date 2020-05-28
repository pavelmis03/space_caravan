from scenes.menu.base import MenuScene
from drawable_objects.textbox import TextBox
from drawable_objects.list_widget import ListWidget


class WorldChoiceMenuScene(MenuScene):
    def __init__(self, game):
        super().__init__(game)
        self.interface_objects.append(TextBox(self, self.game.controller, (100, 100, 500, 150), "Enter text!"))
        import random
        self.interface_objects.append(ListWidget(self, self.game.controller, (100, 200, 500, 500), 25, [
            str(random.randint(0, 1000000)) for _i in range(50)
        ]))

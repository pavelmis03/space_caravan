from drawable_objects.interface.display_count import DisplayCount
from constants.color import COLOR

class AmmoDisplay(DisplayCount):
    """
    Класс для отображения количества патронов
    """
    COLOR = COLOR['WHITE']
    FIELDS = ['magazine', 'ammo']

    def __init__(self, scene, controller, pos, weapon):
        super().__init__(scene, controller, pos, weapon, AmmoDisplay.FIELDS)

    def process_logic(self):
        self.subject = self.scene.player.weapon
        if self.subject.is_reloading:
            render_string = 'Перезарядка: ' + str(self.subject.is_reloading)
        else:
            render_string = '/'.join(self.get_render_data())
        self.render_text(render_string)
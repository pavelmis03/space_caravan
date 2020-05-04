from drawable_objects.interface.display_count import DisplayCount


class AmmoDisplay(DisplayCount):
    """
    Класс для отображения количества патронов
    """
    COLOR = (120, 120, 120)
    FIELDS = ['magazine', 'ammo']

    def __init__(self, scene, controller, pos, weapon):
        super().__init__(scene, controller, pos, weapon, AmmoDisplay.FIELDS)

    def process_logic(self):
        if self.subject.is_reloading:
            render_string = 'Перезарядка...'
        else:
            render_string = '/'.join(self.get_render_data())
        self.render_text(render_string)
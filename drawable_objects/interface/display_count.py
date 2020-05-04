from drawable_objects.base import AbstractObject
from drawable_objects.text import Text


class DisplayCount(AbstractObject):
    """
    Класс для отображения счетчика патронов/топлива

    subject - объект, поля которого ослеживаются
    fields  - отслеживаемые поля объекта
    """
    def __init__(self, scene, controller, pos, subject, fields=[]):
        super().__init__(scene, controller)
        self.subject = subject
        self.fields = fields
        self.text = Text(scene, pos, '')
        self.render_string = None

    def process_logic(self):
        render = []
        for attr in self.fields:
            render.append(str(self.subject.__getattribute__(attr)))
        render_string = '/'.join(render)
        if self.render_string != render_string:
            self.render_string = render_string
            self.text.update_text(render_string)

    def process_draw(self):
        self.text.process_draw()
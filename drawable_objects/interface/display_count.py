from drawable_objects.base import AbstractObject
from drawable_objects.text import Text


class DisplayCount(AbstractObject):
    """
    Класс для отображения счетчика патронов/топлива

    subject - объект, поля которого ослеживаются
    fields  - отслеживаемые поля объекта
    """
    COLOR = (220, 220, 220)

    def __init__(self, scene, controller, pos, subject, fields=[]):
        super().__init__(scene, controller)
        self.subject = subject
        self.fields = fields
        self.text = Text(scene, pos, '', self.COLOR, 'left',
                         'Consolas', 50, False, False)
        self.render_string = None

    def process_logic(self):
        render = self.get_render_data()
        render_string = ' '.join(render)
        self.render_text(render_string)

    def get_render_data(self) -> list:
        """
        Получить все данные, необходимые для рендеринга
        :return: список строк
        """
        render = []
        for attr in self.fields:
            render.append(str(self.subject.__getattribute__(attr)))
        return render

    def render_text(self, render_string):
        """
        Отрендерить строку
        :param render_string: строка
        """
        if self.render_string != render_string:
            # little optimization
            self.render_string = render_string
            self.text.update_text(render_string)

    def process_draw(self):
        self.text.process_draw()

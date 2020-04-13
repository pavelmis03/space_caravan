from drawable_objects.base import DrawableObject
from drawable_objects.text import Text
from geometry.point import Point


class MultilineText(DrawableObject):
    """
    Надпись на экране игры
    В отличие от обычного Text умеет работать с строками,
    содержащими перенос строки

    Хранение осуществляется списком из Text

    Класс имеет скудный функционал, но большего нам пока и не нужно
    """

    def __init__(self, scene, pos, text='Define\nme!', color=(255, 255, 255), align='left', font_name='Comic Sans',
                 font_size=35, is_bold=True, is_italic=False, width_limit=None):
        super().__init__(scene, None, pos)
        self.text_params = {
            'color': color,
            'align': align,
            'font_name': font_name,
            'font_size': font_size,
            'is_bold': is_bold,
            'is_italic': is_italic,
            'width_limit': width_limit
        }
        self.set_text(text)

    def set_text(self, text):
        """
        Задает отображаемый многострочный текст
        :param text: текст
        """
        self.text = []
        for i, line in enumerate(text.split('\n')):
            newtxt = Text(self.scene, self.pos + Point(0, i *
                                                       self.text_params['font_size']), line, **self.text_params)
            self.text.append(newtxt)

    def process_draw(self):
        for txt in self.text:
            txt.process_draw()

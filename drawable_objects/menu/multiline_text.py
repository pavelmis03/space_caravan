from drawable_objects.base import DrawableObject
from drawable_objects.menu.text import Text
from geometry.point import Point
from geometry.rectangle import Rectangle


class MultilineText(DrawableObject):
    """
    Надпись на экране игры
    В отличие от обычного Text умеет работать с строками,
    содержащими перенос строки

    Хранение осуществляется списком из Text

    LINE_OFFSET - дополнительный промежуток между строчками
    """
    LINE_OFFSET = 3

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
        if not text:
            return
        splited = text.split('\n')
        self.text = [
            Text(self.scene, self.pos, splited[0], **self.text_params)
        ]
        offset = self.text[0].text_surface.get_height() + \
            MultilineText.LINE_OFFSET
        for i, line in list(enumerate(splited))[1:]:
            newtxt = Text(self.scene, self.pos +
                          Point(0, i * offset),
                          line, **self.text_params)
            self.text.append(newtxt)

    @property
    def geometry(self):
        rect = Rectangle(0, 0, self.width, self.height)
        rect.top_left = Point(self.pos.x - self.width / 2, self.pos.y)
        return rect

    @property
    def width(self):
        mx = 0
        for text in self.text:
            new_w = text.text_surface.get_width()
            if new_w > mx:
                mx = new_w
        return mx

    @property
    def height(self):
        return (self.text[0].text_surface.get_height() + MultilineText.LINE_OFFSET) * len(self.text)

    def move(self, movement):
        """
        Передвигает текст параллельным переносом на заданный вектор.
        :param movement: вектор переноса
        """
        for text in self.text:
            text.pos += movement
        self.pos += movement

    def process_draw(self):
        for txt in self.text:
            txt.process_draw()

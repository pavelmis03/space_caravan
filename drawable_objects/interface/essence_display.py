from constants.color import COLOR
from drawable_objects.interface.display_count import DisplayCount
from geometry.point import Point


class EssenceDisplay(DisplayCount):
    """
    Класс для отображения количества эссенции клонов
    """
    COLOR = COLOR['BLUE']
    FIELDS = ['essence']

    def __init__(self, scene, controller, pos_ratio, common_data):
        super().__init__(scene, controller, Point(0, 0), common_data, EssenceDisplay.FIELDS)
        self.__pos_ratio = pos_ratio
        self.text.align = 'right'

    def process_logic(self):
        self.render_text(''.join(self.get_render_data()))
        self.text.pos = self.__get_pos()

    def __get_pos(self) -> Point:
        TRANSITION = Point(-40, 20)

        result = Point(self.scene.game.width * self.__pos_ratio[0],
                       self.scene.game.height * self.__pos_ratio[1])
        result += TRANSITION
        return result
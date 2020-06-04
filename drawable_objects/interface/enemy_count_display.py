from typing import Tuple
from drawable_objects.interface.display_count import DisplayCount
from constants.color import COLOR
from geometry.point import Point


class EnemyCountDisplay(DisplayCount):
    """
    Класс для отображения количества патронов
    """
    COLOR = COLOR['RED']

    def __init__(self, scene, controller, pos_ratio: Tuple[float, float], enemy_list):
        super().__init__(scene, controller, Point(0, 0), enemy_list, None)
        self.__pos_ratio = pos_ratio
        self.text.align = 'right'

    def process_logic(self):
        res = str(len(self.subject))
        self.render_text(res)

        self.text.pos = self.__get_pos()

    def __get_pos(self) -> Point:
        TRANSITION = Point(-40, 20)

        result = Point(self.scene.game.width * self.__pos_ratio[0],
                       self.scene.game.height * self.__pos_ratio[1])
        result += TRANSITION
        return result


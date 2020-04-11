from drawable_objects.base import AbstractObject
from drawable_objects.button import Button
from geometry.point import Point


class ButtonGroup(AbstractObject):
    """
    Класс для динамического выравнивания кнопок по центру

    :param scene: сцена, на которой кнопка находится
    :param controller: контроллер
    :param offset: оффсет центра в процентах [(0-1), (0-1)] относительно размеров окна
    :param button_geometry: размеры создаваемых кнопок
    :param button_offset: расстояние между кнопками
    """
    def __init__(self, scene, controller, offset, button_geometry, button_offset=0):
        super().__init__(scene, controller)
        self.pos = [
            self.scene.game.width * offset[0],
            self.scene.game.height * offset[1]
        ]
        self.offset = offset
        self.button_geometry = button_geometry
        self.button_offset = button_offset
        self.buttons = []

    def add_button(self, text, function, kwargs={}):
        geometry = [
            self.pos[0] - self.button_geometry[0] // 2,
            self.pos[1] + (len(self.buttons) - 0.5) * self.button_geometry[1] + len(self.buttons) * self.button_offset,
            self.pos[0] + self.button_geometry[0] // 2,
            self.pos[1] + (len(self.buttons) + 0.5) * self.button_geometry[1] + len(self.buttons) * self.button_offset,
        ]
        btn = Button(self.scene, self.controller, geometry, text, function, kwargs)
        self.buttons.append(btn)

    def recalc_pos(self):
        """
        Перерасчет позиций кнопок для выравнивания по центру (относительно оффсета)
        """
        newpos = [
            self.scene.game.width * self.offset[0],
            self.scene.game.height * self.offset[1]
        ]
        if self.pos != newpos:
            self.move(Point(
                newpos[0] - self.pos[0],
                newpos[1] - self.pos[1]
            ))
            self.pos = newpos

    def move(self, movement):
        """
        Передвигает группу кнопок параллельным переносом на заданный вектор.

        :param movement: вектор переноса
        """
        for button in self.buttons:
            button.move(movement)

    def update_offset(self, offset):
        self.offset = offset
        self.recalc_pos()


    def process_logic(self):
        self.recalc_pos()
        for button in self.buttons:
            button.process_logic()

    def process_draw(self):
        for button in self.buttons:
            button.process_draw()
from drawable_objects.base import AbstractObject
from geometry.point import Point


class Weapon(AbstractObject):

    MAIN_BUTTON = 1
    ALTERNATIVE_BUTTON = 2

    def __init__(self, shooter):
        super().__init__(shooter.scene, shooter.controller)
        self.is_working = True
        self.cooldown_time = 5
        self.cooldown = 0
        self.length = shooter.HITBOX_RADIUS + 1
        print(self.length)

    def process_logic(self):
        if self.cooldown:
            self.cooldown -= 1
            if self.cooldown == 0:
                self.is_working = True
        button = self.controller.get_click_button()
        if button is not None and self.is_working:
            self.manager(button)

    def manager(self, button):
        if button == Weapon.MAIN_BUTTON:
            self.main_attack()
        if button == Weapon.ALTERNATIVE_BUTTON:
            self.alternative_attack()

    def main_attack(self):
        self.attack(self.scene.player.pos, self.scene.player.angle)
        pass

    def alternative_attack(self):
        pass

    def attack(self, pos: Point, angle: float):
        pass
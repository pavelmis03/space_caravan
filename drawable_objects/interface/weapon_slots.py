from drawable_objects.base import SpriteObject, DrawableObject
from geometry.point import Point


class WeaponSlot(SpriteObject):

    def __init__(self, player, pos, weapon_slots_ind):
        self.weapon_slots_ind = weapon_slots_ind
        super().__init__(player.scene, player.controller, player.weapon_slots[weapon_slots_ind].interface_image, pos, zoom=0.75)

    def process_logic(self):
        self.image_name = self.scene.player.weapon_slots[self.weapon_slots_ind].interface_image


class WeaponsDisplay(DrawableObject):

    def __init__(self, player, pos):
        super().__init__(player.scene, player.controller, pos)
        self.weapon_slots = [WeaponSlot(player, Point(pos.x + 30, pos.y + 40), 0),
                             WeaponSlot(player, Point(pos.x + 100, pos.y + 40), 1)]

    def process_logic(self):
        for slot in self.weapon_slots:
            slot.process_logic()

    def process_draw(self):
        for slot in self.weapon_slots:
            slot.process_draw()


from drawable_objects.base import SpriteObject, DrawableObject
from geometry.point import Point


class WeaponsDisplay(DrawableObject):
    """
    Дисплей, отображающий какое оружие выбрано
    """

    def __init__(self, player, pos):
        super().__init__(player.scene, player.controller, pos)
        self.weapon_slots = [WeaponSlot(player, Point(pos.x + 30, pos.y + 40), 0),
                             WeaponSlot(player, Point(pos.x + 110, pos.y + 40), 1)]
        self.choosen_slot = ChoosenSlot(self)

    def process_logic(self):
        self.choosen_slot.process_logic()
        for slot in self.weapon_slots:
            slot.process_logic()

    def process_draw(self):
        self.choosen_slot.process_draw()
        for slot in self.weapon_slots:
            slot.process_draw()


class WeaponSlot(SpriteObject):
    """
    Один слот отображения оружия
    """
    def __init__(self, player, pos, weapon_slots_ind):
        self.weapon_slots_ind = weapon_slots_ind
        super().__init__(player.scene, player.controller, player.weapon_slots[weapon_slots_ind].interface_image, pos)

    def process_logic(self):
        self.image_name = self.scene.player.weapon_slots[self.weapon_slots_ind].interface_image


class ChoosenSlot(SpriteObject):
    """
    Объект для обозначения выбранного слота оружия
    """
    def __init__(self, weapons_display):
        super().__init__(weapons_display.scene, weapons_display.controller, 'interface.choosen_weapon_slot',
                         weapons_display.weapon_slots[0].pos, zoom=1.1)
        self.weapons_display = weapons_display

    def process_logic(self):
        self.pos = self.weapons_display.weapon_slots[self.scene.player.weapon_slots_ind].pos


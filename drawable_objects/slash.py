from drawable_objects.base import GameSprite
from drawable_objects.enemy import Enemy
from geometry.segment import Segment
from drawable_objects.bullet import dist
from math import pi, atan2


class PlayerSlash(GameSprite):
    """
    Базовый удар ближним оружием игрока
    """

    IMAGE_NAMES = [
        'moving_objects.melee_weapon.attack.heavy_splash.1',
        'moving_objects.melee_weapon.attack.heavy_splash.2',
        'moving_objects.melee_weapon.attack.heavy_splash.3',
    ]

    def __init__(self, creator: GameSprite, blade_length):
        super().__init__(creator.scene, creator.controller, self.IMAGE_NAMES[0],
                         creator.pos, creator.angle)
        self.length = blade_length
        self.zoom = blade_length / 430 * 2
        self.creator = creator
        self.image_ind = 0
        self.one_frame_vision_time = 2
        self.damage = 200

    def process_logic(self):
        self.collision_manager()
        self.sprite_manager()

    def collision_manager(self):
        neighbours = self.scene.plane.get_neighbours(self.creator.pos, Enemy)
        for neighbour in neighbours:
            vector_to_neighbour = neighbour.pos - self.creator.pos
            neighbour_to_attacker_angle = atan2(-vector_to_neighbour.y, vector_to_neighbour.x)
            reach = 1.5
            neighbour_to_attacker_angle_range = [neighbour_to_attacker_angle - reach,
                                                 neighbour_to_attacker_angle + reach]
            is_angle_correct = False
            if neighbour_to_attacker_angle_range[1] > pi and \
                    (neighbour_to_attacker_angle_range[0] < self.creator.angle <= pi or
                     -pi <= self.creator.angle < neighbour_to_attacker_angle_range[1] - 2 * pi):
                is_angle_correct = True
            elif neighbour_to_attacker_angle_range[0] < -pi and \
                    (-pi <= self.creator.angle < neighbour_to_attacker_angle_range[1] or
                     neighbour_to_attacker_angle_range[0] + 2 * pi < self.creator.angle <= pi):
                is_angle_correct = True
            elif neighbour_to_attacker_angle_range[0] \
                    < self.creator.angle < \
                    neighbour_to_attacker_angle_range[1]:
                is_angle_correct = True
            if dist(neighbour.pos, self.creator.pos) <= self.length + neighbour.HITBOX_RADIUS and is_angle_correct:
                segment_to_neighbour = Segment(self.creator.pos, neighbour.pos)
                if self.scene.grid.intersect_seg_walls(segment_to_neighbour) is None:
                    neighbour.get_damage(self.damage, neighbour_to_attacker_angle)

    def sprite_manager(self):
        self.image_name = self.IMAGE_NAMES[self.image_ind // self.one_frame_vision_time]
        self.image_ind += 1
        if self.image_ind // self.one_frame_vision_time == len(self.IMAGE_NAMES) - 1:
            self.damage = 0
        else:
            self.pos = self.creator.pos
            self.angle = self.creator.angle
            if self.image_ind >= len(self.IMAGE_NAMES) * self.one_frame_vision_time:
                self.destroy()


class EnemySlash(PlayerSlash):
    """
    Базовый удар ближним оружием Enemy
    """

    def collision_manager(self):
        if dist(self.creator.pos, self.scene.player.pos) <= self.length:
            self.scene.player.get_damage(self.damage)
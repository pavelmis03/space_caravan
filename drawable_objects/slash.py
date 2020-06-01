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
        self.damage = 250
        self.reach = 1.5

    def process_logic(self):
        if not self.creator.enabled:
            self.destroy()
        self.collision_manager()
        self.sprite_manager()

    def is_angle_correct(self, neighbour):
        vector_to_neighbour = neighbour.pos - self.creator.pos
        neighbour_to_attacker_angle = atan2 (-vector_to_neighbour.y, vector_to_neighbour.x)
        neighbour_to_attacker_angle_range = [neighbour_to_attacker_angle - self.reach,
                                             neighbour_to_attacker_angle + self.reach]
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
        return is_angle_correct, neighbour_to_attacker_angle

    def collision_manager(self):
        neighbours = self.scene.plane.get_neighbours(self.creator.pos, Enemy)
        for neighbour in neighbours:
            is_angle_correct, neighbour_to_attacker_angle = self.is_angle_correct(neighbour)
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


class Punch(PlayerSlash):
    """
    Удар кулаком
    """

    IMAGE_NAMES = [
        'moving_objects.melee_weapon.attack.light_splash.11',
        'moving_objects.melee_weapon.attack.light_splash.22',
        'moving_objects.melee_weapon.attack.light_splash.44',
    ]

    def __init__(self, creator: GameSprite, length):
        super().__init__(creator, length)
        self.zoom = 0.5
        self.damage = 25
        self.reach = 1
        self.scene.player.image_name = 'moving_objects.Punch'

    def process_logic(self):
        super().process_logic()
        self.damage = 0

    def destroy(self):
        self.scene.player.image_name = 'moving_objects.PlayerBarehanded'
        super().destroy()
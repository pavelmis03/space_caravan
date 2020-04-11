from drawable_objects.base import GameSprite
from geometry.point import Point
from geometry.segment import Segment
from geometry.vector import vector_from_length_angle
from scenes.base import Scene
from controller.controller import Controller


def create_bullet(shooter: GameSprite):
    bullet = Bullet(shooter.scene, shooter.controller, shooter.pos, shooter.angle)
    shooter.scene.game_objects.append(bullet)


class Bullet(GameSprite):

    IMAGE_ZOOM = 0.7
    IMAGE_NAME = 'moving_objects.bullet.1' # нужно перерисовать
    SPEED = 100

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        super().__init__ (scene, controller, Bullet.IMAGE_NAME, pos, angle, Bullet.IMAGE_ZOOM)
        self.direction = vector_from_length_angle(Bullet.SPEED, self.angle)

    def process_logic(self):
        next_pos = self.pos + self.direction
        self.collision_manager(next_pos)
        self.move(next_pos)

    def collision_manager(self, next_pos: Point):
        if self.scene.grid.is_out_of_grid(self.pos):
            self.destroy()
            return

        trajectory = Segment(self.pos, next_pos)
        intersect_point = self.scene.grid.intersect_seg_walls(trajectory)
        if intersect_point is not None:
            self.collision_with_wall(intersect_point)

    def collision_with_wall(self, collision_point):
        self.scene.game_objects.append(Collision_Point(self.scene, self.controller, collision_point, self.angle))
        self.destroy()

    def is_colliding_with_entities(self):
        pass

    def collision_with_entity(self):
        pass


class Collision_Point(Bullet):
    IMAGE_ZOOM = 0.5

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        self.speed = 0
        self.bullet_type = 'bullet'
        self.lifetime = 200
        angle = angle
        super().__init__(scene, controller, pos, angle)

    def process_logic(self):
        self.lifetime -= 1
        if (self.lifetime <= 0):
            self.destroy()
        pass

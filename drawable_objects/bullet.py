from drawable_objects.base import MovingGameSprite, GameSprite
from geometry.point import Point
from geometry.segment import Segment
from scenes.base import Scene
from controller.controller import Controller

def create_bullet(shooter: GameSprite):
    bullet = Bullet(shooter.scene, shooter.controller, shooter.pos, shooter.angle)
    shooter.scene.game_objects.append(bullet)

class Bullet(MovingGameSprite):

    IMAGE_ZOOM = 0.7

    def __init__(self, scene: Scene, controller: Controller, pos: Point, angle: float = 0):
        BULLET_SPEED = 100
        BULLET_TYPE = 'bullet'
        super().__init__ (scene, controller, BULLET_TYPE, pos, BULLET_SPEED, angle, Bullet.IMAGE_ZOOM)
        self.direction = self.get_direction_vector()

    def process_logic(self):
        next_pos = self.pos + self.direction
        self.collision_manager(next_pos)
        self.move(next_pos)

    def collision_manager(self, next_pos: Point):
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

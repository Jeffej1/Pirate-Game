import pygame, math, random
from entity.entity import *
from ..timer import Timer
from..projectile import Projectile

class BoatEnemy(Entity):
    def __init__(self, assets, pos= (0, 0), player_pos= (0, 0), load_values= None):
        super().__init__()
        self.assets = assets
        self.image = self.assets.get("enemy_boat")
        self.original = self.image
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(pos)
        self.zlayer = 4

        self.player_pos = player_pos
        self.treasure = random.randint(0, 2)
        self.plank = 5 if random.random() < 0.1 else 2

        self.angle = 0
        self.health = self.max_health = 15
        self.cannonballs = pygame.sprite.Group()
        self.direction = pygame.Vector2(0, 0)
        self.invincible = False

        if load_values is not None:
            for key, value in load_values.items():
                if key == "direction" or key == "pos" or key == "player_pos":
                    value = pygame.Vector2(value)
                setattr(self, key, value)
            self.image = pygame.transform.rotate(self.original, self.angle)

        self.cooldown = Timer(1_500)
        self.damage_cooldown = Timer(1_000)

    def get_turn_direction(self, current_angle, target_angle) -> int:
        delta = (((target_angle - current_angle) + 180) % 360) - 180

        if delta > 0:
            return 1
        if delta < 0:
            return -1
        return 0

    def rotate_to_player(self):
        self.desired_angle = int(math.degrees(math.atan2(self.dy, self.dx)) + 270) % 360

        self.angle += self.get_turn_direction(self.angle, self.desired_angle) 

        self.image = pygame.transform.rotate(self.original, self.angle)

    def avoid_player(self):
        turn_direction = self.get_turn_direction(self.angle, self.desired_angle)
        self.angle -= turn_direction if turn_direction != 0 else 1
        self.image = pygame.transform.rotate(self.original, self.angle)

    def boat_movement(self):
        self.dx, self.dy = self.player_pos - self.pos

        if math.hypot(self.dx, self.dy) >= 400:
            self.rotate_to_player()
        else:
            self.avoid_player()

        self.direction.x = -math.sin(math.radians(self.angle))
        self.direction.y = math.cos(math.radians(self.angle))
        self.direction = self.direction.normalize()
        self.pos +=  1.75 * self.direction

    def invincibility(self):
        if self.damage_cooldown.finished():
            self.invincible = False
            self.damage_cooldown.reset()

    def shoot_at_player(self):
        if self.cooldown.finished() and math.hypot(self.dx, self.dy) <= 1000:
            self.cannonballs.add(Projectile(self.assets, self.pos, self.angle, self.player_pos))
            self.cooldown.reset()

    def update(self):
        self.boat_movement()
        self.shoot_at_player()

        if self.invincible:
            self.invincibility()

        if self.border_collision():
            self.remove_health(5)
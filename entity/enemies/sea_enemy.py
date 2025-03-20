import pygame, math, random
from entity.entity import *
from ..timer import Timer

class SeaEnemy(Entity):
    def __init__(self, assets, pos= (0, 0), player_pos= (0, 0), upgrade= False, load_values= None):
        super().__init__()
        self.image = assets.get("shark")
        self.original = self.image
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(pos)
        self.zlayer = 4
        self.rotation = 0

        self.player_pos = player_pos
        self.treasure = random.randint(0, 1)
        self.plank = 0
        self.upgrade = upgrade

        self.health = self.max_health = 5
        self.invincible = False

        if load_values is not None:
            for key, value in load_values.items():
                if key == "pos" or key == "player_pos":
                    value = pygame.Vector2(value)
                setattr(self, key, value)

        self.damage_cooldown = Timer(500)
        self.attack_cooldown = Timer(750)

    def move_to_player(self):
        dx, dy = self.player_pos - self.pos
        angle = math.degrees(math.atan2(dy, dx)) + 180
        if self.rotation != angle:
            self.rotation = angle
            self.image = pygame.transform.rotate(self.original, self.rotation)

        dist = math.hypot(dx, dy)

        if dist > 75:
            self.pos += pygame.Vector2(dx, dy).normalize() * 3

    def update(self):
        self.move_to_player()
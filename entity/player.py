import pygame, math
from .projectile import *
from .entity import *
from .timer import *

class Player(Entity):
    def __init__(self, player_assets: pygame.surface.Surface, load_values= None):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.width, self.height = self.display.get_size()
        self.assets = player_assets
        self.image = self.assets.get("boat")
        self.rect = self.image.get_rect()
        self.original = self.image
        self.zlayer = 5

        self.health = 100
        self.treasure = 0
        self.ammo = self.max_ammo = 4
        self.vel = self.angle = 0
        self.pos = pygame.Vector2(0,0)

        COOLDOWN_DURATION, RELOAD_DURATION, INVINCIBILITY_DURATION = 500, 600, 2_000
        self.loaded_cannonball = True
        self.cannonballs = pygame.sprite.Group()
        self.reloading = False
        
        
        if load_values is not None:
            for key, value in load_values.items():
                if key == "pos":
                    value = pygame.Vector2(value)
                if value is type(dict):
                    value = None
                setattr(self, key, value)
            self.image = pygame.transform.rotate(self.original, self.angle)

        self.reload_timer = Timer(RELOAD_DURATION)
        self.cooldown_timer = Timer(COOLDOWN_DURATION)
        self.damage_cooldown = Timer(INVINCIBILITY_DURATION)
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        key_down = pygame.key.get_just_pressed()
        mouse = pygame.mouse.get_pressed()

        if keys[pygame.K_w] and self.vel < 2.2: # MAX SHOULD BE 2.2
            self.vel += 0.02
        if keys[pygame.K_a]:
            self.image = pygame.transform.rotate(self.original, self.angle)
            self.angle += 1.5
        if keys[pygame.K_s] and self.vel > -2:
            self.vel -= 0.02
        if keys[pygame.K_d]:
            self.image = pygame.transform.rotate(self.original, self.angle)
            self.angle -= 1.5
        if keys[pygame.K_SPACE] and self.vel != 0:
            if self.vel > 0:
                self.vel -= 0.05
            elif self.vel < 0:
                self.vel += 0.05

        if keys[pygame.K_r] and self.reload_timer.finished() and self.ammo < self.max_ammo:
            self.reloading = True
            self.reload_timer.reset()

        if self.reloading:
            self.reload_proj()

        if self.angle >= 360: self.angle = 0
        elif self.angle <= -1: self.angle = 359

        if mouse[0] and self.loaded_cannonball:
            self.fire_proj()
            self.loaded_cannonball = False
            self.cooldown_timer.reset()

        if key_down[pygame.K_j]:
            self.remove_health(5)
        if key_down[pygame.K_k]:
            self.add_health(5)

    def fire_proj(self):
        if self.ammo > 0 and self.reload_timer.finished():
            self.cannonballs.add(Projectile(self.assets, self.pos, self.angle, accel= self.accel, friendly= True))
            self.ammo -= 1

    def reload_proj(self):
        if self.ammo < self.max_ammo and self.reload_timer.finished():
            self.ammo += 1
            if self.ammo < self.max_ammo:
                self.reload_timer.reset()
            else:
                self.reloading = False

    def proj_cooldown(self):
        if self.cooldown_timer.finished():
            self.loaded_cannonball = True

    def move(self):
        if -0.01 <= self.vel <= 0.01:
            self.vel = 0

        self.accel = self.vel ** 3 / 4

        self.pos.x -= self.accel * math.sin(math.radians(self.angle))
        self.pos.y += self.accel * math.cos(math.radians(self.angle))
        
    def update(self):
        self.get_input()
        self.move()
        self.proj_cooldown()
        self.cannonballs.update()

        if self.border_collision() and self.damage_cooldown.finished():
            self.damage_cooldown.reset()
            self.remove_health(5)
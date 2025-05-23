import pygame, math
from .projectile import *
from .entity import *
from .timer import *

class Player(Entity):
    def __init__(self, assets, sounds, load_values= None):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.assets = assets
        self.sounds = sounds

        self.image = self.assets.get("boat")
        self.rect = self.image.get_rect()
        self.original = self.image
        self.zlayer = 5

        self.health = 100
        self.treasure = 0
        self.ammo = self.max_ammo = 4
        self.vel = self.angle = 0
        self.max_vel = 2.2
        self.rotation_speed = 1.5
        self.pos = pygame.Vector2(0,0)
        
        INVINCIBILITY_DURATION = 2_000
        self.reload_duration = 600
        self.cooldown_duration = 500
        self.loaded_cannonball = True
        self.reloading = False
        
        self.max_upgrades = False
        self.upgrades = { # All the upgrades the player can get along with how many they have
            "max_ammo": 0,
            "reload_speed": 0,
            "rotation_speed": 0,
            "max_speed": 0,
            "proj_cooldown": 0,
            }

        if load_values is not None: # If a save is available load the values
            for key, value in load_values.items():
                if key == "pos":
                    value = pygame.Vector2(value)
                setattr(self, key, value)
            self.image = pygame.transform.rotate(self.original, self.angle)

        self.cannonballs = pygame.sprite.Group()
        self.reload_timer = Timer(self.reload_duration)
        self.cooldown_timer = Timer(self.cooldown_duration)
        self.damage_cooldown = Timer(INVINCIBILITY_DURATION)
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        key_down = pygame.key.get_just_pressed()
        mouse = pygame.mouse.get_pressed()

        # Player movement and rotation
        if keys[pygame.K_w] and self.vel < self.max_vel: 
            self.vel += 0.02
        if keys[pygame.K_a]:
            self.image = pygame.transform.rotate(self.original, self.angle)
            self.angle += self.rotation_speed
        if keys[pygame.K_s] and self.vel > -self.max_vel - 0.2:
            self.vel -= 0.02
        if keys[pygame.K_d]:
            self.image = pygame.transform.rotate(self.original, self.angle)
            self.angle -= self.rotation_speed
        if keys[pygame.K_SPACE] and self.vel != 0:
            if self.vel > 0:
                self.vel -= 0.05
            elif self.vel < 0:
                self.vel += 0.05

        if keys[pygame.K_r] and self.reload_timer.finished() and self.ammo < self.max_ammo: # Start reloading
            self.reloading = True
            self.reload_timer.reset()

        if self.reloading: # Reload after R is pressed
            self.reload_proj()

        # Reset angles if they go out of bounds
        if self.angle >= 360: self.angle = 0
        elif self.angle <= -1: self.angle = 359

        if mouse[0] and self.loaded_cannonball: # Fire projectile if the user left clicks and the player has ammo
            self.fire_proj()
            self.loaded_cannonball = False
            self.cooldown_timer.reset()

    def fire_proj(self):
        """
        Fire the cannonball if ready
        """
        if self.ammo > 0 and self.reload_timer.finished():
            self.cannonballs.add(Projectile(self.assets, self.pos, self.angle, accel= self.accel, friendly= True))
            self.ammo -= 1
            self.sounds.play("cannonball")

    def reload_proj(self):
        """
        Continuously reload ammo until the player is back at max ammo
        """
        if self.ammo < self.max_ammo and self.reload_timer.finished():
            self.ammo += 1
            if self.ammo < self.max_ammo:
                self.reload_timer.reset()
            else:
                self.reloading = False

    def proj_cooldown(self):
        """
        Manages the cooldown between firing projectiles
        """
        if self.cooldown_timer.finished():
            self.loaded_cannonball = True

    def move(self):
        if -0.01 <= self.vel <= 0.01: # Prevents very small values slowly moving the player causing drifting
            self.vel = 0

        self.accel = self.vel ** 3 / 4

        self.pos.x -= self.accel * math.sin(math.radians(self.angle))
        self.pos.y += self.accel * math.cos(math.radians(self.angle))
        
    def update(self):
        self.get_input()
        self.move()
        self.proj_cooldown()
        self.cannonballs.update() # Updates all the cannonballs fired by the player

        if self.border_collision() and self.damage_cooldown.finished(): # Damages the player if they touch the beach
            self.damage_cooldown.reset()
            self.remove_health(5)
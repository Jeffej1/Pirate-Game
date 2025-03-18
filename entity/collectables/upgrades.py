import pygame, constants
from entity import Entity

class Upgrade(Entity):
    def __init__(self, assets, player, pos, name, load_values = None):
        self.assets = assets
        self.player = player
        self.pos = pos
        self.name = name

        if load_values is not None:
            for key, value in load_values.items():
                if key == "pos":
                    value = pygame.Vector2(value)
                setattr(self, key, value)

        self.player_upgrades = {
            "max_ammo": 0,
            "reload_speed": 0,
            "rotation_speed": 0,
            "max_speed": 0,
            "proj_cooldown": 0,
            }

    def on_collect(self):
        if self.player_upgrades[self.name] < constants.MAX_UPGRADES:
            if self.name == "max_ammo":
                self.player.max_ammo += 1
            elif self.name == "reload_speed":
                self.player.reload_duration *= 0.8
                self.player.reload_timer.duration = self.player.reload_duration
            elif self.name == "rotation_speed":
                self.rotation_speed += 0.5
            elif self.name == "max_speed":
                self.max_vel += 0.05
            elif self.name == "proj_cooldown":
                self.player.cooldown_duration *= 0.8
                self.player.cooldown_timer.duration = self.player.cooldown_duration
            self.player_upgrades.get(self.name) += 1

    def update(self):
        if pygame.sprite.spritecollide(self, self.player, True):
            self.on_collect()
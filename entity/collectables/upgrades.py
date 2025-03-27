import pygame, random, constants
from entity import Entity

class Upgrade(Entity):
    def __init__(self, assets, pos= (0, 0), load_values = None):
        super().__init__()
        self.image = assets.get("upgrade")
        self.rect = self.image.get_rect()
        self.zlayer = 5

        self.assets = assets
        self.pos = pygame.Vector2(pos)
        
        if load_values is not None:
            for key, value in load_values.items():
                if key == "pos":
                    value = pygame.Vector2(value)
                setattr(self, key, value)
        
    def decide_upgrade_type(self, player):
        player_upgrades = player.upgrades.copy()
        pop_keys = []
        for key, value in player_upgrades.items():
            if value >= constants.MAX_UPGRADES:
                pop_keys.append(key)
        for key in pop_keys:
            player_upgrades.pop(key)

        if len(player_upgrades) != 0:
            i = random.randint(0, len(player_upgrades) - 1)
            self.name = list(player_upgrades.keys())[i]
        else:
            player.max_upgrades = True
                
    def on_collect(self, player):
        self.decide_upgrade_type(player)
        if player.max_upgrades:
            player.treasure += 5
        else:
            if player.upgrades[self.name] < constants.MAX_UPGRADES:
                if self.name == "max_ammo":
                    player.max_ammo += 1
                    player.ammo = player.max_ammo
                elif self.name == "reload_speed":
                    player.reload_duration *= 0.8
                    player.reload_timer.duration = player.reload_duration
                elif self.name == "rotation_speed":
                    player.rotation_speed += 0.5
                elif self.name == "max_speed":
                    player.max_vel += 0.05
                elif self.name == "proj_cooldown":
                    player.cooldown_duration *= 0.8
                    player.cooldown_timer.duration = player.cooldown_duration
            player.upgrades[self.name] += 1
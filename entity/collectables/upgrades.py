import pygame, random, constants
from entity import Entity

class Upgrade(Entity):
    def __init__(self, assets, player, pos= (0, 0), load_values = None):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill('#E0C0C0')
        self.rect = self.image.get_rect()
        self.zlayer = 5

        self.assets = assets
        self.player = player
        self.pos = pygame.Vector2(pos)

        self.decide_upgrade_type()

        if load_values is not None:
            for key, value in load_values.items():
                if key == "pos":
                    value = pygame.Vector2(value)
                setattr(self, key, value)
        
    def decide_upgrade_type(self):
        # player_upgrades = self.player.upgrades.copy()
        # for key, value in player_upgrades.items():
        #     if value >= constants.MAX_UPGRADES:
        #         player_upgrades.pop(key)

        i = random.randint(0, len(self.player.upgrades) - 1)
        self.name = list(self.player.upgrades.keys())[i]
        print(self.name)
                
    def on_collect(self, player):
        if player.upgrades[self.name] < constants.MAX_UPGRADES:
            if self.name == "max_ammo":
                player.max_ammo += 1
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
        print(self.name)
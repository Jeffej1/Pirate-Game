import pygame, random
from .collectable import Plank, Treasure
from .upgrades import Upgrade

class CollectableManager:
    def __init__(self, assets, sounds, player):
        self.display = pygame.display.get_surface()
        self.assets = assets
        self.sounds = sounds

        self.player = player
        self.all_sprites = pygame.sprite.Group()

        self.health_collected = 0

    def spawn_collectable(self, pos, plank= 0, treasure= 0, upgrade= False):
        """
        Spawns the held collectables randomly within an area of the entity's death location
        """
        for i in range(int(plank)):
            self.all_sprites.add(Plank(self.assets, (pos[0] + random.randint(-50, 50), pos[1] + random.randint(-50, 50))))
        for i in range(int(treasure)):
            self.all_sprites.add(Treasure(self.assets, (pos[0] + random.randint(-50, 50), pos[1] + random.randint(-50, 50))))
        if upgrade:
            self.all_sprites.add(Upgrade(self.assets, (pos[0] + random.randint(-50, 50), pos[1] + random.randint(-50, 50))))

    def collected(self, enemies):
        for sprite in self.all_sprites:
            if pygame.sprite.collide_mask(self.player, sprite):
                if sprite.__class__.__name__ == "Plank" and self.player.health != self.player.max_health:
                    self.health_collected += 1 # Only counts health collected that increased the players health
                if sprite.__class__.__name__ == "Upgrade":
                    self.sounds.play("upgrade")
                else:
                    self.sounds.play("collectable")
                sprite.on_collect(self.player)
                sprite.kill()

            for enemy in enemies: # Checks collisions between collectables and enemies
                if pygame.sprite.collide_mask(enemy, sprite) and isinstance(sprite, Treasure):
                    sprite.on_collect(enemy)
                    sprite.kill()
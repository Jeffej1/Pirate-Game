import pygame, random
from .collectable import Plank, Treasure

class CollectableManager:
    def __init__(self, player):
        self.display = pygame.display.get_surface()
        self.player = player
        self.all_sprites = pygame.sprite.Group()

        self.health_collected = 0

    def spawn_collectable(self, pos, plank = 0, treasure = 0):
        for i in range(int(plank)):
            self.all_sprites.add(Plank((pos[0] + random.randint(-50, 50), pos[1] + random.randint(-50, 50))))
        for i in range(int(treasure)):
            self.all_sprites.add(Treasure((pos[0] + random.randint(-50, 50), pos[1] + random.randint(-50, 50))))

    def collected(self, enemies):
        for sprite in self.all_sprites:
            if pygame.sprite.collide_mask(self.player, sprite):
                if sprite.__class__.__name__ == "Plank":
                    health_collected += 1
                sprite.on_collect(self.player)
                sprite.kill()

            for enemy in enemies:
                if pygame.sprite.collide_mask(enemy, sprite) and isinstance(sprite, Treasure):
                    sprite.on_collect(enemy)
                    sprite.kill()
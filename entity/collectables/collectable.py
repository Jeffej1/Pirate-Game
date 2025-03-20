import pygame, random
from ..entity import Entity

class Plank(Entity):
    def __init__(self, assets, pos):
        super().__init__()
        self.image = pygame.Surface((16, 4))
        self.image.fill('#FFFFFF')
        self.pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect()
        rotation = random.randint(0, 359)
        self.image = pygame.transform.rotate(self.image, rotation)
        self.zlayer = 2

    def on_collect(self, entity):
        entity.add_health(5)
        self.kill()

class Treasure(Entity):
    def __init__(self, assets, pos):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill('#FFFFFF')
        self.pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect()
        rotation = random.randint(0, 359)
        self.image = pygame.transform.rotate(self.image, rotation)
        self.zlayer = 2

    def on_collect(self, entity):
        entity.treasure += 1
        self.kill()

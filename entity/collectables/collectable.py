import pygame, random
from ..entity import Entity

class Plank(Entity):
    def __init__(self, assets, pos= (0, 0), load_values= None):
        super().__init__()
        self.image = assets.get("plank")
        self.pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect()
        rotation = random.randint(0, 359) # Gets a random rotation for the sprite

        if load_values is not None: # If a save is available, load the values
            for key, value in load_values.items():
                if key == "pos":
                    value = pygame.Vector2(value)
                setattr(self, key, value)

        self.image = pygame.transform.rotate(self.image, rotation)
        self.zlayer = 2

    def on_collect(self, entity):
        """
        When collected, increase the health of the entity
        """
        entity.add_health(5)
        self.kill()

class Treasure(Entity):
    def __init__(self, assets, pos= (0, 0), load_values= None):
        super().__init__()
        self.image = assets.get("treasure")
        self.pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect()
        rotation = random.randint(0, 359) # Gets a random rotation for the sprite

        if load_values is not None: # If a save is available, load the values
            for key, value in load_values.items():
                if key == "pos":
                    value = pygame.Vector2(value)
                setattr(self, key, value)

        self.image = pygame.transform.rotate(self.image, rotation)
        self.zlayer = 2

    def on_collect(self, entity):
        """
        When collected, increase the treasure of the entity
        """
        entity.treasure += 1
        self.kill()

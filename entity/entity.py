import pygame, constants

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.zlayer = 1
        self.pos = pygame.Vector2(0, 0)
        self.max_health: float = 100
        self.health: float = 100

    def remove_health(self, health_removed: float):
        self.health -= health_removed
        self.health_check()

    def add_health(self, health_added: float):
        self.health += health_added
        self.health = self.max_health if self.health > self.max_health else self.health

    def health_check(self, kill_entity= True):
        if self.health <= 0:
            if kill_entity:
                self.kill()
            return True
        return False

    def border_collision(self):
        collided = False
        if self.pos.x >= constants.BORDER_DIST: 
            self.pos.x = constants.BORDER_DIST
            collided = True
        if self.pos.x <= -constants.BORDER_DIST: 
            self.pos.x = -constants.BORDER_DIST
            collided = True
        if self.pos.y >= constants.BORDER_DIST:
            self.pos.y = constants.BORDER_DIST
            collided = True
        if self.pos.y <= -constants.BORDER_DIST: 
            self.pos.y = -constants.BORDER_DIST
            collided = True

        if collided:
            return True
        return False
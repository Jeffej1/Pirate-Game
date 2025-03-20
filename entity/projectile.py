import pygame, math, constants
from .entity import Entity
from .timer import Timer

class Projectile(Entity):
    def __init__(self, assets, pos: pygame.Vector2= (0, 0), angle= 0,  player_pos: pygame.Vector2= (0, 0), accel= 1, friendly= False, load_values= None):
        super().__init__()
        self.assets = assets
        self.image = self.assets.get("cannonball")
        self.splash_surf = self.assets.get("cannonball_splash")
        self.rect = self.image.get_rect()

        self.zlayer = 2
        self.friendly = friendly
        self.mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        self.pos = pygame.Vector2(pos)
        self.player_pos = pygame.Vector2(player_pos)
        self.accel = float(accel)
        self.angle = int(angle)

        if load_values is not None:
            for key, value in load_values.items():
                if key == "pos" or key == "player_pos" or key == "mouse_pos":
                    value = pygame.Vector2(value)
                setattr(self, key, value)

        self.dead = False
        self.death_timer = Timer(5000)
        
        if self.friendly:
            self.get_direction_to_mouse()
        else:
            self.get_direction_to_player()

    def get_direction_to_player(self):
        dx, dy = self.player_pos - self.pos
        angle = math.atan2(dy, dx)
        self.direction = (math.cos(angle) * 5, math.sin(angle) * 5)

    def get_direction_to_mouse(self):
        dx, dy = self.mouse_pos - pygame.Vector2(constants.WIDTH / 2, constants.HEIGHT / 2)
        angle = math.atan2(dy, dx)
        self.direction = (math.cos(angle) * 5, -math.sin(angle) * 5)

    def move(self):
        self.pos += self.direction
        self.pos.x -= self.accel * math.sin(math.radians(self.angle)) / 3
        self.pos.y += self.accel * math.cos(math.radians(self.angle)) / 3

    def splash(self):
        self.image = self.splash_surf
        self.splash_timer = Timer(500)
        self.dead = True

    def death_countdown(self):
        if not self.dead and self.death_timer.finished():
            self.splash()
        elif not self.dead:
            self.move()
        elif self.dead and self.splash_timer.finished():
            self.kill()

    def border_collision(self):
        if -constants.BORDER_DIST >= self.pos.x or self.pos.x >= constants.BORDER_DIST:
            if not self.dead:
                self.splash()
        if -constants.BORDER_DIST >= self.pos.y or self.pos.y >= constants.BORDER_DIST:
            if not self.dead:
                self.splash()

    def update(self):
        self.death_countdown()
        self.border_collision()
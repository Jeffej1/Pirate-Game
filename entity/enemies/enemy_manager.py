import pygame, random, math, config
from ..entity import Entity
from .boat_enemy import BoatEnemy
from .sea_enemy import SeaEnemy
from ..collectables.collectable_manager import CollectableManager
from ..timer import Timer

class EnemyManager:
    def __init__(self, assets, player):
        self.display = pygame.display.get_surface()
        self.width, self.height = self.display.get_size()
        self.assets = assets

        self.player = player
        self.player_pos = player.pos
        self.player_proj = player.cannonballs

        self.boat_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.proj_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.boat_spawn_timer = Timer(10_000)
        self.water_spawn_timer = Timer(5_000)

        self.max_water = 2
        self.max_boat = 2
        self.total_killed = self.boat_killed = self.water_killed = 0

        self.collectables = CollectableManager(self.player)

    def enemy_collisions(self):
        for enemy in self.enemy_group:
            enemy_type = enemy.__class__.__name__
            if pygame.sprite.spritecollide(enemy, self.player_proj, True) and not enemy.invincible:
                enemy.remove_health(5)
                enemy.invincible = True
            if pygame.sprite.collide_mask(enemy, self.player) and not enemy.invincible:
                if enemy_type == "BoatEnemy":
                    self.player.remove_health(5)
                    enemy.invincible = True
                    enemy.remove_health(5)
                elif enemy_type == "SeaEnemy":
                    if enemy.attack_cooldown.finished():
                        self.player.remove_health(5)
                        enemy.remove_health(1)
                        enemy.attack_cooldown.reset()

            if enemy.health_check():
                self.total_killed += 1
                if enemy_type == "BoatEnemy":
                    self.boat_killed +=1
                elif enemy_type == "SeaEnemy":
                    self.water_killed += 1
                self.collectables.spawn_collectable(enemy.pos, plank= enemy.plank, treasure= enemy.treasure)

        for proj in self.proj_group:
            if pygame.sprite.collide_mask(self.player, proj):
                proj.kill()
                self.player.remove_health(5)
                
    def border_collision(self, x_pos, y_pos):
        collided = False
        if x_pos >= config.border_dist: 
            x_pos = config.border_dist
            collided = True
        if x_pos <= -config.border_dist: 
            x_pos = -config.border_dist
            collided = True
        if y_pos >= config.border_dist:
            y_pos = config.border_dist
            collided = True
        if y_pos <= -config.border_dist: 
            y_pos = -config.border_dist
            collided = True

        if collided:
            return True
        return False

    def get_spawn_pos(self) -> pygame.Vector2:
        spawn_direction = random.randint(1, 4)

        if spawn_direction == 1: # LEFT
            x_start = self.player_pos.x - self.width / 2 - 500
            x_end = x_start + 450
            y_start = self.player_pos.y - self.height / 2 - 500
            y_end = self.player_pos.y + self.height / 2 + 500
        elif spawn_direction == 2: # RIGHT
            x_start = self.player_pos.x + self.width / 2 + 50
            x_end = x_start + 450
            y_start = self.player_pos.y - self.height / 2 - 500
            y_end = self.player_pos.y + self.height / 2 + 500
        elif spawn_direction == 3: # DOWN
            x_start = self.player_pos.x - self.width / 2 - 500
            x_end = self.player_pos.x + self.width / 2 + 500
            y_start = self.player_pos.x - self.height / 2 - 500
            y_end = y_start + 450
        elif spawn_direction == 4: # UP
            x_start = self.player_pos.x - self.width / 2 - 500
            x_end = self.player_pos.y + self.width / 2 + 500
            y_start = self.player_pos.y + self.height / 2 + 50
            y_end = y_start + 450

        x_pos = random.randrange(int(x_start), int(x_end))
        y_pos = random.randrange(int(y_start), int(y_end))

        if self.border_collision(x_pos, y_pos):
            x_pos, y_pos = self.get_spawn_pos()

        return pygame.Vector2((x_pos, y_pos))

    def spawning_enemies(self):
        if self.boat_spawn_timer.finished() and len(self.boat_group.sprites()) != self.max_boat:
            self.boat_group.add(BoatEnemy(self.assets, self.get_spawn_pos(), self.player_pos))
            self.enemy_group.add(self.boat_group.sprites()[-1])
            self.all_sprites.add(self.boat_group)
            self.boat_spawn_timer.reset()
        elif self.boat_spawn_timer.finished() and len(self.boat_group.sprites()) == self.max_boat:
            self.boat_spawn_timer.reset()

        if self.water_spawn_timer.finished() and len(self.water_group.sprites()) != self.max_water:
            self.water_group.add(SeaEnemy(self.assets.get("shark"), self.get_spawn_pos(), self.player_pos))
            self.enemy_group.add(self.water_group.sprites()[-1])
            self.all_sprites.add(self.water_group)
            self.water_spawn_timer.reset()
        elif self.water_spawn_timer.finished() and len(self.water_group.sprites()) == self.max_boat:
            self.water_spawn_timer.reset()

    def update(self):
        self.spawning_enemies()
        self.all_sprites.update()
        self.collectables.collected(self.boat_group)
        self.enemy_collisions()

        for boat in self.boat_group:
            self.proj_group.add(boat.cannonballs)
            self.all_sprites.add(boat, boat.cannonballs)
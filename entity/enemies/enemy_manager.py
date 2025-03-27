import pygame, random, math, constants
from ..entity import Entity
from .boat_enemy import BoatEnemy
from .sea_enemy import SeaEnemy
from ..collectables.collectable_manager import CollectableManager
from ..timer import Timer

class EnemyManager:
    def __init__(self, assets, sounds, player):
        self.display = pygame.display.get_surface()
        self.assets = assets
        self.sounds = sounds

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

        self.max_water = 3
        self.max_boat = 2
        self.total_killed = self.boat_killed = self.water_killed = 0
        self.enemies_spawned = 0
        self.upgrade_due = False

        self.collectables = CollectableManager(self.assets, self.sounds, self.player)

    def enemy_collisions(self):
        for enemy in self.enemy_group:
            enemy_type = enemy.__class__.__name__
            if pygame.sprite.spritecollide(enemy, self.player_proj, True) and not enemy.invincible:
                enemy.remove_health(5)
                enemy.invincible = True
                self.sounds.play("hit")
            if pygame.sprite.collide_mask(enemy, self.player) and not enemy.invincible:
                if enemy_type == "BoatEnemy":
                    self.player.remove_health(5)
                    enemy.invincible = True
                    enemy.remove_health(5)
                    self.sounds.play("hit")
                elif enemy_type == "SeaEnemy":
                    if enemy.attack_cooldown.finished():
                        self.player.remove_health(5)
                        enemy.remove_health(1)
                        enemy.attack_cooldown.reset()
                        self.sounds.play("hit")

            if enemy.health_check():
                self.total_killed += 1
                if enemy_type == "BoatEnemy":
                    self.boat_killed +=1
                elif enemy_type == "SeaEnemy":
                    self.water_killed += 1
                self.sounds.play("enemy_death")
                self.collectables.spawn_collectable(enemy.pos, plank= enemy.plank, treasure= enemy.treasure, upgrade= enemy.upgrade)

        for proj in self.proj_group:
            if pygame.sprite.collide_mask(self.player, proj):
                proj.kill()
                self.player.remove_health(5)
                self.sounds.play("hit")
                
    def border_collision(self, x_pos, y_pos):
        collided = False
        if x_pos >= constants.BORDER_DIST: 
            x_pos = constants.BORDER_DIST
            collided = True
        if x_pos <= -constants.BORDER_DIST: 
            x_pos = -constants.BORDER_DIST
            collided = True
        if y_pos >= constants.BORDER_DIST:
            y_pos = constants.BORDER_DIST
            collided = True
        if y_pos <= -constants.BORDER_DIST: 
            y_pos = -constants.BORDER_DIST
            collided = True

        if collided:
            return True
        return False
    
    def get_upgrade(self):
        if (self.enemies_spawned + 1) % 3 == 0:
            self.upgrade_due = True
        
        if self.upgrade_due:
            self.upgrade_due = False
            return True
        return False

    def get_spawn_pos(self) -> pygame.Vector2:
        spawn_direction = random.randint(1, 4)

        if spawn_direction == 1: # LEFT
            x_start = self.player_pos.x - constants.WIDTH / 2 - 500
            x_end = x_start + 450
            y_start = self.player_pos.y - constants.HEIGHT / 2 - 500
            y_end = self.player_pos.y + constants.HEIGHT / 2 + 500
        elif spawn_direction == 2: # RIGHT
            x_start = self.player_pos.x + constants.WIDTH / 2 + 50
            x_end = x_start + 450
            y_start = self.player_pos.y - constants.HEIGHT / 2 - 500
            y_end = self.player_pos.y + constants.HEIGHT / 2 + 500
        elif spawn_direction == 3: # DOWN
            x_start = self.player_pos.x - constants.WIDTH / 2 - 500
            x_end = self.player_pos.x + constants.WIDTH / 2 + 500
            y_start = self.player_pos.x - constants.HEIGHT / 2 - 500
            y_end = y_start + 450
        elif spawn_direction == 4: # UP
            x_start = self.player_pos.x - constants.WIDTH / 2 - 500
            x_end = self.player_pos.y + constants.WIDTH / 2 + 500
            y_start = self.player_pos.y + constants.HEIGHT / 2 + 50
            y_end = y_start + 450

        x_pos = random.randrange(int(x_start), int(x_end))
        y_pos = random.randrange(int(y_start), int(y_end))

        if self.border_collision(x_pos, y_pos):
            x_pos, y_pos = self.get_spawn_pos()

        return pygame.Vector2((x_pos, y_pos))

    def spawning_enemies(self):
        if self.boat_spawn_timer.finished() and len(self.boat_group.sprites()) != self.max_boat:
            self.boat_group.add(BoatEnemy(self.assets, self.get_spawn_pos(), self.player_pos, self.get_upgrade()))
            self.enemy_group.add(self.boat_group.sprites()[-1])
            self.all_sprites.add(self.boat_group)
            self.boat_spawn_timer.reset()
            self.enemies_spawned += 1
        elif self.boat_spawn_timer.finished() and len(self.boat_group.sprites()) == self.max_boat:
            self.boat_spawn_timer.reset()

        if self.water_spawn_timer.finished() and len(self.water_group.sprites()) != self.max_water:
            self.water_group.add(SeaEnemy(self.assets, self.get_spawn_pos(), self.player_pos, self.get_upgrade()))
            self.enemy_group.add(self.water_group.sprites()[-1])
            self.all_sprites.add(self.water_group)
            self.water_spawn_timer.reset()
            self.enemies_spawned += 1
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
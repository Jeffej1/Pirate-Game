import pygame
from .cursor import Cursor

class Hud:
    def __init__(self, player):
        self.display = pygame.display.get_surface()
        self.width, self.height = self.display.get_size()
        self.extra_active = False
        self.player = player
        self.cursor = Cursor()
        self.font = pygame.font.SysFont('segoeuiblack', 30)

    def display_health(self):
        health_width = self.player.health * 5
        health_border_width = self.player.max_health * 5
        health_colour = '#B02020'
        health_text = self.font.render(f"{self.player.health} / {self.player.max_health}", True, '#000000')
        health_rect = health_text.get_rect(topright = (health_border_width, 20))

        # RED HEALTH BOX
        pygame.draw.rect(self.display, health_colour, (10, 20, health_width, 50))

        # MISSING HEALTH BACKGROUND
        if self.player.health != self.player.max_health:
            health_background_width = (self.player.max_health - self.player.health) * 5
            health_background_left = health_width + 10
            pygame.draw.rect(self.display, '#505050', (health_background_left, 20, health_background_width, 50))

        # HEALTH BOX BORDER
        pygame.draw.rect(self.display, '#141414', (5, 15, health_border_width + 10, 60), 10, 10)

        self.display.blit(health_text, health_rect)
        
    def display_ammo(self):
        for i in range(self.player.ammo):
            pygame.draw.circle(self.display, '#181c1c', (self.width - 30 - 42 * i, self.height - 30), 20)

        if self.player.ammo == 0:
            no_ammo_text = self.font.render("NO AMMO - 'R' TO RELOAD", True, '#141414')
            no_ammo_rect = no_ammo_text.get_rect(midright = (self.width - 30, self.height - 30))
            self.display.blit(no_ammo_text, no_ammo_rect)

    def display_treasure(self):
        treasure_text = self.font.render(f"TREASURE: {self.player.treasure * 5}", True, '#202020')
        treasure_rect = treasure_text.get_rect(right = self.width - 5)

        self.display.blit(treasure_text, treasure_rect)
    
    def check_f3(self):
        key_down = pygame.key.get_just_pressed()
        if key_down[pygame.K_F3]:
            if self.extra_active:
                self.extra_active = False
            elif not self.extra_active:
                self.extra_active = True

    def extra_info(self, fps: int):
        # DISPLAY FPS
        fps_text = self.font.render(str(fps), True, '#202020')
        fps_rect = fps_text.get_rect(topleft = (5, 70))
        self.display.blit(fps_text, fps_rect)

        # DISPLAY POSITION
        pos_text = self.font.render(str(self.player.pos), True, '#202020')
        pos_rect = pos_text.get_rect(topleft = (5, 95))
        self.display.blit(pos_text, pos_rect)

    def update(self, fps: float):
        self.width, self.height = self.display.get_size()

        self.check_f3()
        if self.extra_active:
            self.extra_info(int(fps))
        self.display_ammo()
        self.display_health()
        self.display_treasure()
        self.cursor.update()
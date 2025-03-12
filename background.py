import pygame, config

class Background(pygame.sprite.Sprite):
    def __init__(self, assets):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.width, self.height = self.display.get_size()
        self.water = assets.get("water")
        self.beach = assets.get("beach")
        self.zlayer = 0

        self.pos = pygame.Vector2(0,0)

        self.draw_image()

    def draw_image(self):
        water_diameter = 2 * config.border_dist
        beach_section = pygame.Surface((water_diameter + self.width, self.width / 2))
        water_section = pygame.Surface((water_diameter, water_diameter))

        for x in range(0, water_section.get_width(), 128):
            for y in range(0, water_section.get_height(), 128):
                water_section.blit(self.water, (x, y))

        for x in range(0, beach_section.get_width(), 16):
            for y in range(0, beach_section.get_height(), 16):
                beach_section.blit(self.beach, (x, y))

        self.image = pygame.Surface((beach_section.get_width(), beach_section.get_width()))
        self.image.blit(water_section, water_section.get_rect(topleft = (self.width / 2, self.width / 2)))
        self.image.blit(beach_section, (0, 0))
        self.image.blit(pygame.transform.rotate(beach_section, 90), beach_section.get_rect())
        self.image.blit(pygame.transform.rotate(beach_section, 180), beach_section.get_rect(bottom = self.image.get_height()))
        self.image.blit(pygame.transform.rotate(beach_section, 270), beach_section.get_rect(left = self.image.get_height() - self.width / 2))
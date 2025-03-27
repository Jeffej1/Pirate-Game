import pygame, constants

class Background(pygame.sprite.Sprite):
    def __init__(self, assets):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.water = assets.get("water")
        self.beach = assets.get("beach")
        self.zlayer = 0

        self.pos = pygame.Vector2(0,0)

        self.draw_image()

    def draw_image(self):
        water_diameter = 2 * constants.BORDER_DIST
        beach_section = pygame.Surface((water_diameter + constants.WIDTH, constants.WIDTH / 2))
        water_section = pygame.Surface((water_diameter, water_diameter))

        for x in range(0, water_section.get_width(), self.water.get_width()):
            for y in range(0, water_section.get_height(), self.water.get_height()):
                water_section.blit(self.water, (x, y))

        for x in range(0, beach_section.get_width(), self.beach.get_width()):
            for y in range(0, beach_section.get_height(), self.beach.get_height()):
                beach_section.blit(self.beach, (x, y))

        self.image = pygame.Surface((beach_section.get_width(), beach_section.get_width()))
        self.image.blit(water_section, water_section.get_rect(topleft = (constants.WIDTH / 2, constants.WIDTH / 2)))
        self.image.blit(beach_section, (0, 0))
        self.image.blit(pygame.transform.rotate(beach_section, 90), beach_section.get_rect())
        self.image.blit(pygame.transform.rotate(beach_section, 180), beach_section.get_rect(bottom = self.image.get_height()))
        self.image.blit(pygame.transform.rotate(beach_section, 270), beach_section.get_rect(left = self.image.get_height() - constants.WIDTH / 2))
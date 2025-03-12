import pygame

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.mouse.set_visible(False)
        self.display = pygame.display.get_surface()
        self.original = self.image = pygame.image.load("./assets/crosshair.png")
        self.rect = self.image.get_rect()
        self.rotation = 0

    def draw_cursor(self):
        self.rect.center = pygame.mouse.get_pos()
        self.display.blit(self.image, self.rect)
        
    def update(self):
        current_cursor = pygame.mouse.get_cursor()[0]
        if current_cursor == pygame.SYSTEM_CURSOR_HAND and self.rotation > -45:
            self.rotation -= 5
            self.image = pygame.transform.rotate(self.original, self.rotation)
            self.rect = self.image.get_rect()
        elif current_cursor == pygame.SYSTEM_CURSOR_ARROW and self.rotation < 0:
            self.rotation += 5
            self.image = pygame.transform.rotate(self.original, self.rotation)
            self.rect = self.image.get_rect()

        self.draw_cursor()
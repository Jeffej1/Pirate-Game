import pygame, sys, scenes, constants
from scenes.scenemanager import SceneManager

class MainGame:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT)) # Makes the window with a size 1600x900
        pygame.display.set_caption("PIRATE GAME")
        self.scene_manager = SceneManager()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.scene_manager.quit_game()

            self.scene_manager.draw()
            pygame.display.update()

if __name__ == "__main__":
    MainGame().run()
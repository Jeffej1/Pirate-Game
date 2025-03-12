import pygame, sys, scenes
from scenes.scenemanager import SceneManager

class MainGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1600, 900
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("YARGHHH")
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

# TODO
# UPGRADES?
# SOUND
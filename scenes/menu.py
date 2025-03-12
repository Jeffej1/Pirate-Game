import pygame, sys
from ui import *

class MenuScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.display = pygame.display.get_surface()
        self.image = self.scene_manager.load_asset("main_menu")
        self.rect = self.image.get_rect()
        self.width, self.height = self.display.get_size()
        self.cursor = Cursor()

        play_button = Button((self.width - 500, self.height / 2 - 250), 450, 200, '#A06020', '#602000', '#C08040', "PLAY", self.game_scene, 15, 30, 80)
        continue_button = Button((self.width - 500, self.height / 2), 450, 200, '#A06020', '#602000', '#C08040', "CONTINUE", self.load_game, 15, 30, 70)
        quit_button = Button((self.width - 475, self.height - 200), 400, 150, '#A06020', '#602000', '#C08040', "QUIT", self.quit_game, 15, 30, 60)
        settings_button = Button((25, 20), 125, 50, '#808080', '#202020', '#A0A0A0', "OPTIONS", self.settings_scene, 10, 40, 20)

        gui = {
            "play": play_button,
            "continue": continue_button,
            "quit": quit_button,
            "settings": settings_button
            }
        self.ui_manager = UIManager(gui)

    def game_scene(self):
        self.scene_manager.change_scene("game")

    def load_game(self):
        self.scene_manager.scene_list["game"].load_game()
        self.scene_manager.change_scene("game")

    def settings_scene(self):
        self.scene_manager.change_scene("settings")

    def quit_game(self):
        self.scene_manager.quit_game()

    def update(self):
        self.display.fill((0, 32, 224))
        self.display.blit(self.image, self.rect)

        self.ui_manager.update()
        
        self.cursor.update()
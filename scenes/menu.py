import pygame, sys, constants
from ui import *

class MenuScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.display = pygame.display.get_surface()

        self.image = self.scene_manager.load_asset("main_menu")
        self.rect = self.image.get_rect()
        
        self.cursor = Cursor()

        play_button = Button((constants.WIDTH - 500, constants.HEIGHT / 2 - 250), 450, 200, '#A06020', '#602000', '#C08040', "PLAY", self.game_scene, 15, 30, 80)
        continue_button = Button((constants.WIDTH - 500, constants.HEIGHT / 2), 450, 200, '#A06020', '#602000', '#C08040', "CONTINUE", self.load_game, 15, 30, 70)
        quit_button = Button((constants.WIDTH - 475, constants.HEIGHT - 200), 400, 150, '#A06020', '#602000', '#C08040', "QUIT", self.quit_game, 15, 30, 60)
        settings_button = Button((25, 20), 125, 50, '#808080', '#202020', '#A0A0A0', "OPTIONS", self.settings_scene, 10, 40, 20)

        gui = { # Contains all the buttons for the game
            "play": play_button,
            "continue": continue_button,
            "quit": quit_button,
            "settings": settings_button
            }
        self.ui_manager = UIManager(gui)

        self.scene_manager.sounds.play_music()

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
        self.display.blit(self.image, self.rect) # Displays the background

        self.ui_manager.update() # Checks to see if any of the buttons have been pressed and executes their associated function
        
        self.cursor.update()
import pygame, constants
from ui import *

class GameOverScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.display = pygame.display.get_surface()

        self.cursor = Cursor()

        restart_button = Button((constants.WIDTH / 2 - 500, constants.HEIGHT - 400), 1000, 100, '#A06020', '#602000', '#C08040', "RESTART", self.restart, 15, 20, 50)
        settings_button = Button((constants.WIDTH / 2 - 500, constants.HEIGHT - 275), 1000, 100, '#808080', '#202020', '#A0A0A0', "SETTINGS", self.settings_scene, 15, 20, 50)
        quit_button = Button((constants.WIDTH / 2 - 500, constants.HEIGHT - 150), 1000, 100, '#A06020', '#602000', '#C08040', "QUIT", self.quit_game, 15, 20, 50)

        gui = { # Contains all the buttons
            "restart": restart_button,
            "settings": settings_button,
            "quit": quit_button,
        }
        self.ui_manager = UIManager(gui)

    def quit_game(self):
        self.scene_manager.quit_game()

    def restart(self):
        self.scene_manager.restart_scene("game")
        self.scene_manager.change_scene("game")

    def settings_scene(self):
        self.scene_manager.change_scene("settings")

    def create_score(self) -> float:
        """
        Creates a score value based on certain values/statistics acheived by the player
        """
        score = 0
        score += self.total_killed * 150
        score += self.boat_killed * 50 + self.water_killed * 30
        score += self.treasure * 30
        score -= self.collectables_missed * 33
        score -= self.health_collected * 11
        time_multipler = (self.treasure * 500 / self.time_played)
        collectables_missed_multiplier = 1 - (self.collectables_missed / ((self.treasure / 5) + self.health_collected + self.collectables_missed + 1)) # +1 incase of total collected being 0

        score *= collectables_missed_multiplier
        score *= time_multipler
        return int(score)

    def create_text(self):
        """
        Creates text for the statistics shown
        """
        font = pygame.font.SysFont('segoeuiblack', 50)

        text = f"TREASURE COLLECTED: {self.treasure}\nENEMY BOATS KILLED: {self.boat_killed}\nSHARKS KILLED: {self.water_killed}\nTOTAL KILLED: {self.total_killed}\nPLANKS USED: {self.health_collected}\nCOLLECTABLES MISSED: {self.collectables_missed}"
        score = f"SCORE: {self.create_score()}"

        self.text_surf = font.render(text, True, '#202020')
        self.text_rect = self.text_surf.get_rect(center = (800, 250))
        self.score_surf = font.render(score, True, '#202020')
        self.score_rect = self.score_surf.get_rect(center = (1300, 250))
        
    def display_text(self):
        self.display.blit(self.text_surf, self.text_rect)
        self.display.blit(self.score_surf, self.score_rect)

    def update(self):
        self.display.blit(self.blur_surface, (0, 0)) # Displays a blurred image of the final frame from the game scene before the player died
        self.display_text()
        self.ui_manager.update()
        self.cursor.update()
import pygame, scenes, sys, json
from assetloader import Assets
from soundloader import Sounds
from entity.timer import Timer

class SceneManager:
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.current_scene = "menu"
        self.previous_scene = "menu"
        self.assets = Assets()
        self.sounds = Sounds()
        print(self.sounds.sounds)
        self.popup_active = False
        self.scene_list = {
            "menu": scenes.MenuScene(self),
            "game": scenes.GameScene(self),
            "settings": scenes.SettingsScene(self),
            "end": scenes.GameOverScene(self),
        }

        self.clock = pygame.time.Clock()

    def change_scene(self, new_scene):
        self.previous_scene, self.current_scene = self.current_scene, new_scene
        self.sounds.play("qw3rtyujiycdx")

    def get_current_scene(self):
        return self.current_scene
    
    def restart_scene(self, scene):
        self.scene_list[scene].__init__(self)
    
    def popup(self, text= "ERROR", size= 40, duration_ms= 3000, colour= '#B02020'):
        self.popup_active = True
        self.popup_timer = Timer(duration_ms)
        font = pygame.font.SysFont('segoeuiblack', size)
        self.text_surf = font.render(text, True, '#B02020')
        self.text_rect = self.text_surf.get_rect(midleft = (20, self.display.get_height() - 30))

    def display_popup(self):
        if not self.popup_timer.finished():
            self.display.blit(self.text_surf, self.text_rect)
        else:
            self.popup_active = False

    def load_asset(self, asset_name) -> pygame.surface.Surface:
        return self.assets.get(asset_name)

    def quit_game(self):
        pygame.quit()
        sys.exit()
    
    def draw(self):
        self.scene_list[self.current_scene].update()
        if self.popup_active:
             self.display_popup()

        self.clock.tick(60)
import pygame, json
from ui import *

class SettingsScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.display = pygame.display.get_surface()
        self.width, self.height = self.display.get_size()
        self.cursor = Cursor()

        self.read_cfg()

        master_volume = Slider((500, 250), 0, 100, self.master, '#804010', '#602000', '#905020', '#A06020', "Master Volume", 600, font_size = 50)
        music_volume = Slider((500, 400), 0, 100, self.music, '#804010', '#602000', '#905020', '#A06020', "Music Volume", 600, font_size = 50)
        effect_volume = Slider((500, 550), 0, 100, self.effect, '#804010', '#602000', '#905020', '#A06020', "Effect Volume", 600, font_size = 50)
        back_button = Button((25, 20), 125, 50, '#808080', '#202020', '#A0A0A0', "BACK", self.back_scene, 10, 40, 20)
        gui = {
            "master": master_volume,
            "music": music_volume,
            "effect": effect_volume,
            "back": back_button
            }
        self.ui_manager = UIManager(gui)

    def back_scene(self):
        self.change_cfg()
        self.scene_manager.change_scene(self.scene_manager.previous_scene)

    def read_cfg(self):
        with open("./settings.cfg", "r") as cfg:
            try:
                data = json.load(cfg)
                for key, value in data.items():
                    setattr(self, key, value)
            except:
                self.master = self.effect = self.music = 50 #If no 'settings.cfg' file is found or unreadable by json module
            cfg.close()

    def change_cfg(self):
        with open("./settings.cfg", "w") as cfg:
            values = {}
            for key, value in self.ui_manager.gui.items():
                if isinstance(value, Slider):
                    values[key] = value.current_value
            data = json.dumps(values, indent= 4)
            cfg.write(data)
            cfg.close()

    def update(self):
        self.display.fill('#404040')
        
        self.ui_manager.update()

        self.cursor.update()
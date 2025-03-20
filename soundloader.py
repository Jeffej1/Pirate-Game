import pygame, os

class Sounds:
    def __init__(self):
        self.sounds = {}
        self.load()

    def load(self):
        for dir, _, file_names in os.walk("assets/sounds"):
            for file in file_names:
                if file.split(".")[-1] == "wav":
                    self.sounds[file.split(".")[0]] = pygame.mixer.Sound(f"{dir}/{file}")

    def play(self, sound_name):
        self.sounds.get(sound_name, self.sounds["error"]).play()
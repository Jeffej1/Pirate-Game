import pygame, os

class Sounds:
    def __init__(self):
        self.sounds = {}
        self.load()

    def load(self):
        for dir, _, file_names in os.walk("assets/sounds"):
            for file in file_names:
                split_file = file.split(".")
                if split_file[-1] == "wav":
                    self.sounds[split_file[0]] = pygame.mixer.Sound(f"{dir}/{file}")
                elif split_file[-1] == "mp3":
                    #self.sounds[split_file[0]] = pygame.mixer_music.load(f"{dir}/{file}")
                    pygame.mixer_music.load(f"{dir}/{file}")

    def set_volume(self, master_volume, music_volume, effect_volume):
        master_volume /= 100
        music_volume *= master_volume / 100
        effect_volume *= master_volume / 100

        for sound in self.sounds.values():
            sound.set_volume(effect_volume)
        pygame.mixer_music.set_volume(music_volume)

    def play(self, sound_name):
        self.sounds.get(sound_name, self.sounds["error"]).play()

    def play_music(self):
        pygame.mixer_music.play(-1)
import pygame, os

class Sounds:
    def __init__(self):
        self.sounds = {}
        self.load()

    def load(self):
        for dir, _, file_names in os.walk("assets/sounds"):
            for file in file_names:
                split_file = file.split(".")
                if split_file[-1] == "wav": # Regular sound files are tored as .wav
                    self.sounds[split_file[0]] = pygame.mixer.Sound(f"{dir}/{file}")
                elif split_file[-1] == "mp3": # Music is stored as .mp3
                    pygame.mixer_music.load(f"{dir}/{file}")

    def set_volume(self, master_volume, music_volume, effect_volume):
        # Volumes in pygame are from 0 to 1 so you need to divide by 100 to convert from a percentage to decimal
        master_volume /= 100 
        music_volume *= master_volume / 100
        effect_volume *= master_volume / 100

        for sound in self.sounds.values():
            sound.set_volume(effect_volume)
        pygame.mixer_music.set_volume(music_volume)

    def play(self, sound_name):
        self.sounds.get(sound_name, self.sounds["error"]).play() # Plays the sound or the error sound if the file isn't found

    def play_music(self):
        pygame.mixer_music.play(-1) # Plays the music on loop for the entire game
import pygame, os

class Assets:
    def __init__(self):
        self.assets = {}
        self.load()

    def load(self):
        for dir, _, file_names in os.walk("assets"):
            for file in file_names:
                if file.split(".")[-1] == "png":
                    self.assets[file.split(".")[0]] = pygame.image.load(f"{dir}/{file}").convert_alpha()

    def get(self, asset_name) -> pygame.surface.Surface:
        return self.assets.get(asset_name, self.assets["error"])
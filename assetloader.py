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

    #     self.sort_to_groups()

    # def sort_to_groups(self):
    #     entity_group = ["boat", "cannonball", "cannonball_splash", "enemy_boat", "shark"]
    #     player_group = entity_group[:3]
    #     enemy_group = entity_group[1:]
    #     background_group = ["beach", "water"]

    #     entity_dict = player_dict = enemy_dict = background_dict = {}

    #     entity_dict[(key for key in entity_group)] = self.asset.get(asset for asset in entity_group)
    #     player_dict[(key for key in player_group)] = self.asset.get(asset for asset in player_group)
    #     enemy_dict[(key for key in enemy_group)] = self.asset.get(asset for asset in enemy_group)
    #     background_dict[(key for key in background_group)] = self.asset.get(asset for asset in background_group)

    #     self.groups = {
    #         "entity": entity_dict,
    #         "player": player_dict,
    #         "enemy": enemy_dict,
    #         "background": background_dict,
    #     }
        
    def get(self, asset_name) -> pygame.surface.Surface:
        return self.assets.get(asset_name, self.assets["error"])
    
    # def get_group(self, group_name) -> dict:
    #     return self.group.get(group_name, self.assets["error"])
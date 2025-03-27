import pygame, json, copy, constants
from entity import *
from ui import *
from assetloader import Assets
from background import Background
from camera import Camera
from entity.enemies.enemy_manager import EnemyManager

class GameScene:
    def __init__(self, scene_manager, load_values= None):
        self.scene_manager = scene_manager
        self.display = pygame.display.get_surface()
        self.assets = self.scene_manager.assets
        self.sounds = self.scene_manager.sounds

        if load_values is not None:
            for i in load_values:
                if i["type"] == "Player":
                    self.player = Player(self.assets, self.sounds, load_values= i)
                    self.enemy_manager = EnemyManager(self.assets, self.scene_manager.sounds, self.player)
                    print("PLAYER LOADED")
                elif i["type"] == "Projectile":
                    if i["friendly"]:
                        self.player.cannonballs.add(Projectile(self.assets, load_values= i))
                        print("FRIENDLY CANNONBALL LOADED")
                    else:
                        projectile = Projectile(self.assets, load_values= i)
                        self.enemy_manager.proj_group.add(projectile)
                        self.enemy_manager.all_sprites.add(projectile)
                        print("ENEMY CANNONBALL LOADED")
                elif i["type"] == "BoatEnemy":
                    boat = BoatEnemy(self.assets, load_values= i)
                    boat.player_pos = self.enemy_manager.player_pos
                    self.enemy_manager.boat_group.add(boat)
                    self.enemy_manager.enemy_group.add(boat)
                    print("BOAT LOADED")
                elif i["type"] == "SeaEnemy":
                    fish = SeaEnemy(self.assets, load_values= i)
                    fish.player_pos = self.enemy_manager.player_pos
                    self.enemy_manager.water_group.add(fish)
                    self.enemy_manager.enemy_group.add(fish)
                    print("FISH LOADED")
                elif i["type"] == "Plank":
                    self.enemy_manager.collectables.all_sprites.add(Plank(self.assets, load_values= i))
                    print("PLANK LOADED")
                elif i["type"] == "Treasure":
                    self.enemy_manager.collectables.all_sprites.add(Treasure( self.assets, load_values= i))
                    print("TREASURE LOADED")
                elif i["type"] == "Upgrade":
                    self.enemy_manager.collectables.all_sprites.add(Upgrade(self.assets, load_values= i))
                    print("UPGRADE LOADED")
        else:
            self.player = Player(self.assets, self.sounds)
            self.enemy_manager = EnemyManager(self.assets, self.sounds, self.player)

        self.background = Background(self.assets)
        self.camera = Camera(self.player.pos)
        self.hud = HUD(self.player)

        self.paused = False
        self.time_played = 0

        continue_button = Button((constants.WIDTH / 2 - 500, constants.HEIGHT / 2 - 325), 1000, 100, '#A06020', '#602000', '#C08040', "CONTINUE", self.unpause, 15, 20, 50)
        save_button = Button((constants.WIDTH / 2 - 500, constants.HEIGHT / 2 - 175), 1000, 100, '#A06020', '#602000', '#C08040', "SAVE", self.save_game, 15, 20, 50)
        load_button = Button((constants.WIDTH / 2 - 500, constants.HEIGHT / 2 - 25), 1000, 100, '#A06020', '#602000', '#C08040', "LOAD", self.load_game, 15, 20, 50)
        settings_button = Button((constants.WIDTH / 2 - 500, constants.HEIGHT / 2 + 125), 1000, 100, '#808080', '#202020', '#A0A0A0', "SETTINGS", self.settings_scene, 15, 20, 50)
        quit_button = Button((constants.WIDTH / 2 - 500, constants.HEIGHT / 2 + 275), 1000, 100, '#A06020', '#602000', '#C08040', "QUIT", self.quit_game, 15, 20, 50)
        end_button = Button((constants.WIDTH - 100, 100), 100, 100, '#808080', '#202020', '#A0A0A0', "END", self.game_over, 15, 20, 10)

        gui = {
            "continue": continue_button,
            "save": save_button,
            "load": load_button,
            "settings": settings_button,
            "quit": quit_button,
            "end": end_button
        }
        self.ui_manager = UIManager(gui)


    def save_game(self):
        with open('./save.cfg', 'w') as save:
            save_data = []
            sprites = copy.copy(list(self.camera.all_sprites)[1:]) # INDEX 0 WILL ALWAYS BE A BACKGROUND SPRITE SO IT DOESNT NEED TO BE SAVED
            for obj in sprites:
                obj.type = obj.__class__.__name__
                obj.__dict__.pop("assets", "NOT FOUND")
                obj.__dict__.pop("sounds", "NOT FOUND")
                save_data.append(obj)

            data = json.dumps(save_data, cls= SetEncoder, indent= 4)
            save.write(data)
            save.close()
        self.load_game()

    def load_game(self):
        with open('./save.cfg', 'r') as save:
            try:
                save_data = json.load(save)
                self.__init__(self.scene_manager, save_data)
            except:
                self.scene_manager.popup("FILE COULDN'T BE LOADED - SAVE DATA IS EITHER EMPTY OR CORRUPTED")  #If no 'save.cfg' file is found or unreadable by json module

            save.close()

    def settings_scene(self):
        self.scene_manager.change_scene("settings")

    def unpause(self):
        self.paused = False
        self.ui_manager.hovering_any = False

    def game_over(self):
        end_scene = self.scene_manager.scene_list["end"]

        self.camera.render(self.background, self.player, self.player.cannonballs, self.enemy_manager.all_sprites, self.enemy_manager.collectables.all_sprites)
        end_scene.blur_surface = pygame.transform.gaussian_blur(self.display, 2)

        end_scene.collectables_missed = 0
        for sprite in self.enemy_manager.collectables.all_sprites:
            end_scene.collectables_missed +=1

        end_scene.total_killed = self.enemy_manager.total_killed
        end_scene.boat_killed = self.enemy_manager.boat_killed
        end_scene.water_killed = self.enemy_manager.water_killed
        end_scene.health_collected = self.enemy_manager.collectables.health_collected
        end_scene.treasure = self.player.treasure
        end_scene.time_played = self.time_played
        
        end_scene.create_text()
        self.scene_manager.change_scene("end")

    def quit_game(self):
        self.scene_manager.quit_game()

    def update(self):
        p_key_pressed = pygame.key.get_just_pressed()[pygame.K_p]
        if not self.paused:
            self.player.update()
            self.enemy_manager.update()
            self.ui_manager.change_cursor()
            self.camera.update()
            self.camera.render(self.background, self.player, self.player.cannonballs, self.enemy_manager.all_sprites, self.enemy_manager.collectables.all_sprites)

            if self.player.health_check(kill_entity= False):
                self.game_over()

            if p_key_pressed:
                self.blur_surface = pygame.transform.gaussian_blur(self.display, 2)
                self.paused = True

            self.hud.update(self.scene_manager.clock.get_fps())
            self.time_played += 1
        else:
            self.display.blit(self.blur_surface, (0, 0))

            self.ui_manager.update()
            self.hud.update(self.scene_manager.clock.get_fps())

            if p_key_pressed:
                self.unpause()

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pygame.Vector2):
            return tuple(obj) # Can't directly serialise a pygame.Vector2
        if isinstance(obj, Entity):
            obj = obj.__dict__ # Needs to be a dictionary to serialise
            for i in list(obj.keys()):
                if isinstance(obj[i], (pygame.sprite.Group, pygame.surface.Surface, pygame.rect.Rect, dict)) and i != "upgrades":
                    del obj[i] # Attributes that don't need to be saved or can't be serialised
            return obj
        # Not needed to be saved
        if isinstance(obj, timer.Timer):
            return
        return json.JSONEncoder.default(self, obj) # Serialises normally if it isn't any of the above
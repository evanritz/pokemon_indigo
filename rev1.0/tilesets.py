import pygame
import os

class MapStructuresTileset:
    pass

class MapInnerStructuresTileset:
    pass

class MapTexturesTileset:
    def __init__(self, dir):

        self.base_size=(24, 24)
        self.dir = dir

        self.dir_path = os.path.join(self.dir, 'game_assets', 'map_textures')

        GRASS_BASE = 0
        SMALL_WATERFALL = 1

        self.textures = {
            GRASS_BASE: pygame.image.load(os.path.join(self.dir_path, 'grass_base.png')),
            SMALL_WATERFALL: pygame.image.load(os.path.join(self.dir_path, 'waterfall.png'))

        }

    def get_textures(self):
        return self.textures

class MapObjectsTileset:
    pass




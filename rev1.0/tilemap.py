'''
tilemap.py

loads a json file containing the map structure represented by ints

- tilelayer is a 2D array of ints, each item in tilelayer arr representing a row
- structure and object layer give x and y coords and type for texture

{
    "Map": [
        {
            "tilelayer": [
                1: {1, 0, 2, 1, 0, ...},
                2: {0, 1, 2, ...},
                ...
            ]
        },
        {
            "structurelayer": [
                1: {x, y, type}
            ]
        },
        {
            "objectlayber": [
                1: {x, y, type}
            ]
        }
    ]
}


'''

import pygame
import json
import os

from screen_grid import ScreenGrid
from tilesets import MapTexturesTileset


class TileLayer:

    def __init__(self, map_dict, map_textures):
        self.tile_2d_list = map_dict['map']['tilelayer']['layer']
        self.map_textures = map_textures
        self.tiles = []

        self.load()

    def load(self):
        w, h = Tilemap.tile_area
        dx, dy  = Tilemap.map_texture_tile_size
        x0 = y0 = Tilemap.tile_offset

        self.screen_tilelayer = pygame.Surface(Tilemap.tile_area, pygame.SRCALPHA)

        sum = 0
        for x in range(x0, w, dx):
            sum += 1
        print(sum)

        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                row = x//dx
                col = y//dy
                #print(row, col)
                map_texture_type = self.tile_2d_list[row][col]
                if map_texture_type != -1:
                    self.screen_tilelayer.blit(self.map_textures[map_texture_type], (x, y))
    
                #print(x, y)
    def draw(self, screen):
        screen.blit(self.screen_tilelayer, self.screen_tilelayer.get_rect())


class Tilemap:

    map_texture_tile_size = 0
    max_tile_dimensions = 0
    tile_area = 0
    tile_offset = 0
            
    '''
    class StructureLayer:
        pass

    class ObjectLayer:
        pass
    '''

    def __init__(self, map_file_name, dir):
        self.map_file_name = map_file_name
        self.dir = dir 
        
        # create map file path
        self.map_file_path = os.path.join(self.dir, self.map_file_name)

        # load map file into a dict
        with open(self.map_file_path, 'r') as f:
            raw_map_data = f.read()
            self.map_dict = json.loads(raw_map_data)

        # init tilesets and store textures
        self.map_textures = MapTexturesTileset(self.dir).get_textures()

        self.map_texture_tile = self.map_textures[0].get_rect()
       
        Tilemap.map_texture_tile_size = (self.map_texture_tile.w, self.map_texture_tile.h)

        amt_of_tiles = (ScreenGrid.w/self.map_texture_tile.w, ScreenGrid.h/self.map_texture_tile.h)

        tiles_h = (amt_of_tiles[1]-int(amt_of_tiles[1]))*self.map_texture_tile.h 
        tiles_w = (amt_of_tiles[0]-int(amt_of_tiles[0]))*self.map_texture_tile.w

        if tiles_w > tiles_h:
            Tilemap.tile_offset = int(tiles_w)
        else:
            Tilemap.tile_offset = int(tiles_h)

        screen_rect = pygame.Rect(0, 0, ScreenGrid.w, ScreenGrid.h)
        screen_rect_mod = screen_rect.inflate(-Tilemap.tile_offset, -Tilemap.tile_offset)

        Tilemap.tile_area = (screen_rect_mod.w, screen_rect_mod.h)
        print(Tilemap.tile_area)

        self.tilelayer = TileLayer(self.map_dict, self.map_textures)

    def draw(self, screen):
        self.tilelayer.draw(screen)

        




# map.py
#
# Creates tile sprite map from .tmx files
# .tmx files can be created using Tiled
# 
# Loads xml file, parses xml to create Tileset, Layer, Tilemap objects
# Tileset, Layer, Tilemap objects are used to create Tile object lists 
#
# Written by Evan

from dirs import *
from consts import *
from utils import *

import xmltodict
import pygame
import csv
import os

class Map:

    def __init__(self, game, name, file_names):
        
        self.game = game
        self.name = name
        self.should_transition = True

        self.tilemaps = {}
        for file_name in file_names:
            with open(os.path.join(MAPS_DIR, file_name)) as f:
                self.XML_map_raw = xmltodict.parse(f.read())
            name = file_name.split('.')[0]
            self.tilemaps.update({name: Tilemap(self.game, self.XML_map_raw)})

        self.transition(self.name)

    def transition(self, name):
        self.game.floor_tiles.empty()
        self.game.struct_tiles.empty()
        self.game.decor_tiles.empty()
        self.game.shadow_tiles.empty()
        self.game.all_sprites.empty()
        #self.game.all_sprites.add(self.game.player)
        self.tilemaps[name].insert_tiles()
        self.should_transition = False
        

    def get_floor_layer_size(self):
        return self.tilemap.get_floor_layer_size()

class Tilemap:
    def __init__(self, game, XML_map_raw):
        self.game = game
        self.XLM_map = XML_map_raw['map']

        self.w, self.h = int(self.XLM_map['@width']), int(self.XLM_map['@height'])
        
        self.XLM_tilesets = self.XLM_map['tileset']

        self.tilesets = []
        for XLM_tileset in self.XLM_tilesets:
            self.tilesets.append(Tileset(XLM_tileset))

        self.layers = []
        self.XLM_layers = self.XLM_map['layer']
        for layer_level, XLM_layer in enumerate(self.XLM_layers):
            layer = Layer(XLM_layer, layer_level+1)
            layer.create_tiles(self.tilesets)
            self.layers.append(layer)
    
    def insert_tiles(self):
        for layer in self.layers:
            tiles = layer.get_tiles()
            print(layer.id)
            self.game.all_sprites.add(tiles)
            if layer.id == 1:
                self.game.floor_tiles.add(tiles)
            elif layer.id == 2:
                self.game.struct_tiles.add(tiles)
            elif layer.id == 3:
                self.game.decor_tiles.add(tiles)
            elif layer.id == 4:
                self.game.shadow_tiles.add(tiles)
        
    def get_floor_layer_size(self):
        return (self.layers[0].w, self.layers[0].h)


class Tileset:
    def __init__(self, XLM_tileset):
        self.XLM_tileset = XLM_tileset

        self.start_id = int(self.XLM_tileset['@firstgid'])
        self.tile_count = int(self.XLM_tileset['@tilecount'])
        self.end_id = self.start_id+self.tile_count
        self.cols = int(self.XLM_tileset['@columns'])
        self.rows = self.tile_count//self.cols
        
        self.file_name = os.path.split(self.XLM_tileset['image']['@source'])[1]
        self.image_w = int(self.XLM_tileset['image']['@width'])
        self.image_h = int(self.XLM_tileset['image']['@height'])
        self.image = load_image_file(TILESHEETS_DIR, self.file_name)
        #self.image.set_colorkey(pygame.Color('black'))
        self.cut()        

    def cut(self):
        self.id_to_tile = {}
        id = self.start_id
        for y in range(0, self.image_h, SRC_TILE_SIZE):
            for x in range(0, self.image_w, SRC_TILE_SIZE):
                tile = self.image.subsurface((x, y), (SRC_TILE_SIZE, SRC_TILE_SIZE))
                tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
                self.id_to_tile.update({id: tile})
                id += 1

        print(self.id_to_tile)

    def contains_id(self, id):
        return id >= self.start_id and id < self.end_id
        
    def get_tile(self, id):
        return self.id_to_tile[id]

class Layer:
    def __init__(self, XLM_layer, layer_level):
        self.XML_layer = XLM_layer
        self.layer_level = layer_level

        self.name = self.XML_layer['@name']
        self.id = int(self.XML_layer['@id'])
        self.w = int(self.XML_layer['@width'])
        self.h = int(self.XML_layer['@height'])

        map_raw = self.XML_layer['data']['#text'].split(',\n')
        reader = csv.reader(map_raw, delimiter=',')
        self.int_map = [[int(ele) for ele in row] for row in reader]

    def create_tiles(self, tilesets):
        self.tiles = []
        for y, row in enumerate(self.int_map):
            for x, id in enumerate(row):
                for tileset in tilesets:
                    if tileset.contains_id(id):
                        image = tileset.get_tile(id)
                        self.tiles.append(Tile(id, self.layer_level, image, (x*TILE_SIZE, y*TILE_SIZE)))

    def get_tiles(self):
        return self.tiles

class Tile(pygame.sprite.Sprite):
    def __init__(self, id, layer_level, image, coord):
        self._layer = layer_level
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.image = image
        #self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.topleft = coord
        #print(self.rect.x, self.rect.y)
    def draw(self, screen):
        screen.blit(self.image, self.rect)


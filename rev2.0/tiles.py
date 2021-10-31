import pygame
import xmltodict
import csv
import os

from dirs import *

class Tileset:

    def __init__(self, file_name, tileset_id):
        
        self.file_name = file_name
        self.tileset_id = tileset_id

        self.file_path = os.path.join(MAP_TEXTURES_DIR, self.file_name)

        self.image = pygame.image.load(self.file_path)
        self.rect = self.image.get_rect()

        self.tile_size = (16, 16)

        self.calc_coords()

    def calc_coords(self):

        self.coords = []
        self.id_dict = {'0': None}
        self.id = 1

        # cut up tiles by set tile size and store coords
        for y in range(0, self.rect.h, self.tile_size[1]):
            row = [(x, y) for x in range(0, self.rect.w, self.tile_size[0])]
            self.coords.append(row)

        # place coords and id into id dict
        for coord_row in self.coords:
            for coord_pair in coord_row:
                self.id_dict.update({str(self.id): coord_pair})
                self.id += 1

    def get_image(self):
        return self.image

    def get_coord(self, id):
        return self.id_dict[id]

    def get_id(self):
        return self.tileset_id

class Layer:

    def __init__(self, layer, tileset, **kwargs):
        self.layer = layer
        self.tileset = tileset

        self.tile_size = (16, 16)

        if 'scaled_tile_size' in kwargs:
            self.tile_size = kwargs['scaled_tile_size']
        
        self.src_image = self.tileset.get_image()

        text_map = self.layer['data']['#text']
        text_map_rows = text_map.split(',\n')

        reader = csv.reader(text_map_rows, delimiter=',')
        self.int_map = [[ element for element in row] for row in reader]
        
        self.tile_dict = {'0': None}

        self.crop()

    def crop(self):

        for int_map_row in self.int_map:
            for int_map_id in int_map_row:
                
                coord = self.tileset.get_coord(int_map_id)
                if not int_map_id in self.tile_dict.keys() and coord != None:
                    cropped_image = self.src_image.subsurface((*coord, 16, 16))
                    if self.tile_size != (16, 16):
                        cropped_image = pygame.transform.scale(cropped_image, self.tile_size)
                    self.tile_dict.update({int_map_id: cropped_image})
                
    def draw(self, screen):

        w = h = 0
        for int_map_row in self.int_map:
            for int_map_id in int_map_row:       
                tile = self.tile_dict[int_map_id]
                if tile != None:
                    tile_rect = tile.get_rect()
                    tile_rect.topleft = (w, h)
                    screen.blit(tile, tile_rect)
                w += self.tile_size[0] #16
            w = 0
            h += self.tile_size[1]#16

        

class Bound:

    def __init__(self, bounds):

        bounds = bounds['object']

        self.bound_rects = []


        for object in bounds:

            bound = (round(float(object['@x'])), round(float(object['@y'])), round(float(object['@width'])), round(float(object['@height'])))
            bound_rect = pygame.Rect(bound[0]*2, bound[1]*2, bound[2]*2, bound[3]*2)
            self.bound_rects.append(bound_rect)
        
    def get_bound_areas(self):
        return self.bound_rects

class Tilemap:

    def __init__(self, file_name, tilesets):

        self.file_name = file_name
        self.tilesets = tilesets

        self.file_path = os.path.join(GAME_MAPS_DIR, self.file_name)

        with open(self.file_path) as f:
            self.xml_map = xmltodict.parse(f.read())

        map = self.xml_map['map']

        # number of TILES for w and h
        self.w = int(map['@width'])
        self.h = int(map['@height'])

        self.map_layers = map['layer']
        self.bound_layers = map['objectgroup']

        # layers draw tiles to screen
        # bounds define areas

        # layer 1 lower level
        # layer 2 decorations
        # layer 3 na

        # bound 1 map bounding
        # bound 2 pokemon bounding


        self.layers = []
        self.bounds = []

        for map_layer in self.map_layers:
            if map_layer['@id'] == '1':
                self.layers.append(Layer(map_layer, self.tilesets, scaled_tile_size=(32, 32)))
            elif map_layer['@id'] == '2':
                self.layers.append(Layer(map_layer, self.tilesets, scaled_tile_size=(32, 32)))

        for bound_layer in self.bound_layers:
            if bound_layer['@id'] == '3':
                self.bounds.append(Bound(bound_layer))
            elif bound_layer['@id'] == '5':
                self.bounds.append(Bound(bound_layer))


    def get_bounds(self):
        return self.bounds
        
    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)


        # layer 1 = tile layer
        # layer 2 = structures layer
        # layer 3 objects and decerations











from screen_grid import BattleSelectionBox, BattleSelectionItemBox, MainBox, ScreenGrid
from textures import Textures

import numpy
import pygame
import os

class Tileset:

    dir = None
    margin = 0
    spacing = 0

    def __init__(self, type, size=(8, 8), **kwargs):
        
        self.size = size

        if 'dir' in kwargs:
            Tileset.dir = kwargs['dir']

        if 'margin' in kwargs:
            Tileset.margin = kwargs['margin']

        if 'spacing' in kwargs:
            Tileset.spacing = kwargs['spacing']

        GRASS_BASE = 0

        self.textures = {
            #Textures.GRASS: pygame.image.load(os.path.join(dir, Textures.grass_tile)),
            GRASS_BASE: pygame.image.load(os.path.join(Tileset.dir, 'grass_base.png'))
        }


        self.texture = self.textures[type]
        self.rect = self.texture.get_rect()

        self.tiles = []

        self.load()

    def load(self):

        x0 = y0 = Tileset.margin
        w, h = self.rect.size

        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size)
                tile.blit(self.texture, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def get_textures(self):
        return self.textures

class Tilemap:

    def __init__(self, tileset, size=(10, 10), rect=None):
        self.size = size
        self.tileset = tileset
        self.map = numpy.zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface((32*w, 32*h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def draw(self, screen):
        '''
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j*48, i*48))
        screen.blit(self.image, self.rect)
        '''

        tile_size = (96, 96)
        amt_of_tiles = (ScreenGrid.w/tile_size[0], ScreenGrid.h/tile_size[1])

        tiles_h = (amt_of_tiles[1]-int(amt_of_tiles[1]))*tile_size[1] 
        tiles_w = (amt_of_tiles[0]-int(amt_of_tiles[0]))*tile_size[0] 

        fact = 0

        if tiles_w > tiles_h:
            fact = tiles_w
        else:
            fact = tiles_h

        print(amt_of_tiles) 
        print(tiles_h, tiles_w)

        rect = pygame.Rect(0, 0, ScreenGrid.w, ScreenGrid.h)
        rect_mod = rect.inflate(-fact, -fact)

        mb = MainBox()

        mb_img = self.tileset.get_textures()[2]
        mb_img_rect = mb_img.get_rect()
        mb_img = pygame.transform.scale(mb_img, (mb.w, mb.h))
        mb_img_rect = mb_img.get_rect()
        mb_img_rect.center = mb.center
        screen.blit(mb_img, mb_img_rect)
        
        bb = BattleSelectionBox()
        pb = BattleSelectionItemBox('topleft')

        pb_img = self.tileset.get_textures()[2]
        pb_img_rect = pb_img.get_rect()
        pb_img = pygame.transform.scale(pb_img, (pb.w, pb.h))
        pb_img_rect = pb_img.get_rect()
        pb_img_rect.center = pb.center

        #pygame.draw.rect(screen, pygame.Color('white'), pb_img_rect.inflate(12, 12), border_radius=8)
        pygame.draw.rect(screen, pygame.Color('black'), pb_img_rect.inflate(8, 8), border_radius=8)
        screen.blit(pb_img, pb_img_rect)

        pb = BattleSelectionItemBox('topright')

        pb_img = self.tileset.get_textures()[2]
        pb_img_rect = pb_img.get_rect()
        pb_img = pygame.transform.scale(pb_img, (pb.w, pb.h))
        pb_img_rect = pb_img.get_rect()
        pb_img_rect.center = pb.center

        #pygame.draw.rect(screen, pygame.Color('white'), pb_img_rect.inflate(12, 12), border_radius=8)
        pygame.draw.rect(screen, pygame.Color('black'), pb_img_rect.inflate(8, 8), border_radius=8)
        screen.blit(pb_img, pb_img_rect)

        pb = BattleSelectionItemBox('bottomleft')

        pb_img = self.tileset.get_textures()[2]
        pb_img_rect = pb_img.get_rect()
        pb_img = pygame.transform.scale(pb_img, (pb.w, pb.h))
        pb_img_rect = pb_img.get_rect()
        pb_img_rect.center = pb.center

        #pygame.draw.rect(screen, pygame.Color('white'), pb_img_rect.inflate(12, 12), border_radius=8)
        pygame.draw.rect(screen, pygame.Color('black'), pb_img_rect.inflate(8, 8), border_radius=8)
        screen.blit(pb_img, pb_img_rect)

        pb = BattleSelectionItemBox('bottomright')


        pb_img = self.tileset.get_textures()[2]
        pb_img_rect = pb_img.get_rect()
        pb_img = pygame.transform.scale(pb_img, (pb.w, pb.h))
        pb_img_rect = pb_img.get_rect()
        pb_img_rect.center = pb.center


        #pygame.draw.rect(screen, pygame.Color('white'), pb_img_rect.inflate(12, 12), border_radius=8)
        pygame.draw.rect(screen, pygame.Color('black'), pb_img_rect.inflate(8, 8), border_radius=8)
        screen.blit(pb_img, pb_img_rect)


        

        #pygame.draw.rect(screen, pygame.Color('green'), rect)
        #pygame.draw.rect(screen, pygame.Color('blue'), rect_mod)
        
        

    def set_zero(self):
        self.map = numpy.zeros(self.size, dtype=int)
        print(self.map)
        print(self.map.shape)
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = numpy.random.randint(n, size=self.size)
        print(self.map)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'  



import pygame
from tiles import Tilemap, Tileset

from entities import Player

class Game:

    def __init__(self):

        self.tileset1 = Tileset('Overworld.png', 1)
        self.tilemap = Tilemap('test.tmx', self.tileset1)

        self.player = Player((50, 50))

    def move_toggle(self, dir):
        self.player.move_toggle(dir)

    def update(self):
        self.player.update()
    
    def draw(self, screen):
        self.tilemap.draw(screen)
        self.player.draw(screen)

    
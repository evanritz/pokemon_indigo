import pygame
from tiles import Tilemap, Tileset
from entities import Player
from random import randrange

class Game:

    def __init__(self):

        self.tileset1 = Tileset('Overworld.png', 1)
        self.tilemap = Tilemap('map1.tmx', self.tileset1)
        
        self.bounds = self.tilemap.get_bounds()
        self.world_bounds = self.bounds[0].get_bound_areas()
        self.pokemon_bounds = self.bounds[1].get_bound_areas()

        self.player = Player((16*32, 15*32))
        self.player_rect = self.player.get_rect()
        self.player_pos = self.player_rect.center

        self.pokemon_encounter_chance = 33
        self.out_of = 100

        self.prev_ms = 0
        self.delay = 1000*10

        self.fuk_pokemon_check = False

        self.flag = None

    def move_toggle(self, dir):
        self.player.move_toggle(dir)

    def check_flag(self):
        return self.flag

    def update(self):

        if self.flag == 'battle':
            self.prev_ms = pygame.time.get_ticks()
            self.flag = None

        self.player_rect = self.player.get_rect()
        self.player_pos = self.player_rect.center
        for bound in self.world_bounds:
            if self.player_rect.colliderect(bound):
                self.player.set_crossing_bound(True)
                break
            else:
                self.player.set_crossing_bound(False)

        self.curr_ms = pygame.time.get_ticks()
        if self.curr_ms-self.prev_ms >= self.delay:
            self.prev_ms = self.curr_ms
            for bound in self.pokemon_bounds:
                bound_pos = bound.topleft
                #if bound_pos[0] <= self.player_pos[0] and bound_pos[1] >= self.player_pos[1]:
                #    if self.flag != 'battle':
                if self.player_rect.colliderect(bound) and self.flag != 'battle':
                   # if randrange(1, 2000) <= self.pokemon_encounter_chance:
                        self.flag = 'battle'
                        self.player.glitch_fix_moving_toggle()
                        break
        #elif self.flag == 'battle':
        #    self.flag = None
            

        self.player.update()
    
    def draw(self, screen):
        self.tilemap.draw(screen)
        self.player.draw(screen)
       
        #for bound in self.bounds:
        #    pygame.draw.rect(screen, pygame.Color('blue'), bound)

    
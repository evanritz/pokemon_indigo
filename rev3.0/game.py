
# game.py
#
# Holds all init call, event, update, draw loops
# 
# Written by Evan

from consts import *
from keyboard import Keyboard
from entities import Player
from map import Map

import pygame

class Game:
    
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_REZ)
        self.clock = pygame.time.Clock()

        # init keyboard for user input events
        self.keyboard = Keyboard()

        # Game running (Start Screen, Start Intro), Game playing (Game, Battle)
        self.RUNNING, self.PLAYING = True, True#False

        # 1 = Start Screen, 2 = Start Intro, 3 = Game, 4 = Battle 
        self.STATE = 3

        self.game_init()

    def game_init(self):

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.floor_tiles = pygame.sprite.LayeredUpdates()
        self.struct_tiles = pygame.sprite.LayeredUpdates()
        self.decor_tiles = pygame.sprite.LayeredUpdates()
        self.shadow_tiles = pygame.sprite.LayeredUpdates()
        self.entity_sprites = pygame.sprite.LayeredUpdates()

        # init Map object
        self.map = Map(self, 'test2', ['test2.tmx', 'test_inner.tmx'])
        # int Player object
        self.player = Player(self, SCREEN_W//2-PLAYER_SPRITE_SIZE[0]//2, SCREEN_H//2-PLAYER_SPRITE_SIZE[1]//2)

    def game_events(self):

        self.keyboard.get_key_events()
        # Check for pause or exit
        self.RUNNING = not self.keyboard.EXIT_GAME
        self.PLAYING = not self.keyboard.EXIT_GAME

        # Running 
        if self.keyboard.SHIFT:
            # Check key
            if self.keyboard.UP:
                # Move all sprites (Tiles, Entities, etc)
                for sprite in self.all_sprites:
                    sprite.rect.y += PLAYER_RUNNING_VEL
                # Move player back, player is in all_sprites (keep screen on player)
                self.player.vel.y += -PLAYER_RUNNING_VEL
                # Set facing direction
                self.player.facing = 'up'
            elif self.keyboard.DOWN:
                for sprite in self.all_sprites:
                    sprite.rect.y += -PLAYER_RUNNING_VEL
                self.player.vel.y += PLAYER_RUNNING_VEL
                self.player.facing = 'down'
            elif self.keyboard.LEFT:
                for sprite in self.all_sprites:
                    sprite.rect.x += PLAYER_RUNNING_VEL
                self.player.vel.x += -PLAYER_RUNNING_VEL
                self.player.facing = 'left'
            elif self.keyboard.RIGHT:
                for sprite in self.all_sprites:
                    sprite.rect.x += -PLAYER_RUNNING_VEL
                self.player.vel.x += PLAYER_RUNNING_VEL
                self.player.facing = 'right'
        # Walking
        else:
            if self.keyboard.UP: 
                for sprite in self.all_sprites:
                    sprite.rect.y += PLAYER_WALKING_VEL
                self.player.vel.y += -PLAYER_WALKING_VEL        
                self.player.facing = 'up'
            elif self.keyboard.DOWN:
                for sprite in self.all_sprites:
                    sprite.rect.y += -PLAYER_WALKING_VEL
                self.player.vel.y += PLAYER_WALKING_VEL
                self.player.facing = 'down'
            elif self.keyboard.LEFT:
                for sprite in self.all_sprites:
                    sprite.rect.x += PLAYER_WALKING_VEL
                self.player.vel.x += -PLAYER_WALKING_VEL
                self.player.facing = 'left'
            elif self.keyboard.RIGHT:
                for sprite in self.all_sprites:
                    sprite.rect.x += -PLAYER_WALKING_VEL
                self.player.vel.x += PLAYER_WALKING_VEL
                self.player.facing = 'right'

    def game_update(self):
        #self.entity_sprites.update()
        self.all_sprites.update()
        self.reload_sprites()
        #print(self.player.pos)

    # TODO
    def reload_sprites(self):
        if self.map.should_transition:
            self.map.transition('test_inner')
            self.player.rect.y = PLAYER_SPRITE_SIZE[1]
            self.all_sprites.add(self.player)
    
    # Draw all sprites
    def game_draw(self):
        # Set screen to black
        self.screen.fill(pygame.Color('black'))
        # draw all sprites
        self.all_sprites.draw(self.screen)
        # update display
        pygame.display.flip()
        # try to say at set FPS
        self.clock.tick(FPS)

    def game_loop(self):
        self.game_events()
        self.game_update()
        self.game_draw()        

    # TODO
    def battle_loop(self):
        pass

    # Quit game
    def quit(self):
        self.RUNNING = False
        self.PLAYING = False


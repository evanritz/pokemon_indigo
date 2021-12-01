# entities.py
#
# Holds all class defitions of stuff that moves
# 
# Written by Evan

from consts import *
from dirs import *
from pokemon import Pokemon
from utils import *

import pygame
import random
import math

# Player class as a pygame sprite
class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LEVEL
        pygame.sprite.Sprite.__init__(self, game.all_sprites, game.entity_sprites)

        # player pokemon, DEBUG for battlemenu will be selected in game
        # Index 20 choosen for Testing
        self.pokemon = [self.game.pokedex.pokemon[random.randint(0, self.game.pokedex.size-1)]]
        self.encouter_pokemon = None
        # Velocity vector
        self.vel = pygame.Vector2(0, 0)
        # Spawn pos
        self.pos = (x, y)
        # Spawn facing direction
        self.facing = 'down'

        self.animation_idx = 1

        self.load_sprites()

    def load_sprites(self):
        
        # Read json file and load image file
        player_json = load_json_file(SPRITESHEETS_DIR, 'player.json')
        player_image = load_image_file(SPRITESHEETS_DIR, 'player2.png')

        # Parse Json and load all animation frames

        w, h = player_json['size']['w'], player_json['size']['w']
        
        frames = player_json['walking']['up']
        self.walking_up_images = [
            pygame.transform.scale(player_image.subsurface((frames[0]['frame']['x'], frames[0]['frame']['y']), (w, h)),PLAYER_SPRITE_SIZE),
            pygame.transform.scale(player_image.subsurface((frames[1]['frame']['x'], frames[1]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),
            pygame.transform.scale(player_image.subsurface((frames[2]['frame']['x'], frames[2]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),
            pygame.transform.scale(player_image.subsurface((frames[3]['frame']['x'], frames[3]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE)
        ]

        frames = player_json['walking']['left']
        self.walking_left_images = [
            pygame.transform.scale(player_image.subsurface((frames[0]['frame']['x'], frames[0]['frame']['y']), (w, h)),PLAYER_SPRITE_SIZE),
            pygame.transform.scale(player_image.subsurface((frames[1]['frame']['x'], frames[1]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),
            pygame.transform.scale(player_image.subsurface((frames[2]['frame']['x'], frames[2]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),
            pygame.transform.scale(player_image.subsurface((frames[3]['frame']['x'], frames[3]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE)
        ]

        frames = player_json['walking']['down']
        self.walking_down_images = [
            pygame.transform.scale(player_image.subsurface((frames[0]['frame']['x'], frames[0]['frame']['y']), (w, h)),PLAYER_SPRITE_SIZE),
            pygame.transform.scale(player_image.subsurface((frames[1]['frame']['x'], frames[1]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),
            pygame.transform.scale(player_image.subsurface((frames[2]['frame']['x'], frames[2]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),
            pygame.transform.scale(player_image.subsurface((frames[3]['frame']['x'], frames[3]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE)
        ]

        frames = player_json['walking']['right']
        self.walking_right_images = [
            pygame.transform.scale(player_image.subsurface((frames[0]['frame']['x'], frames[0]['frame']['y']), (w, h)),PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[1]['frame']['x'], frames[1]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[2]['frame']['x'], frames[2]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[3]['frame']['x'], frames[3]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE)#.set_colorkey(pygame.Color('white'))
        ]

        frames = player_json['running']['up']
        self.running_up_images = [
            pygame.transform.scale(player_image.subsurface((frames[0]['frame']['x'], frames[0]['frame']['y']), (w, h)),PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[1]['frame']['x'], frames[1]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[2]['frame']['x'], frames[2]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[3]['frame']['x'], frames[3]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE)#.set_colorkey(pygame.Color('white'))
        ]

        frames = player_json['running']['left']
        self.running_left_images = [
            pygame.transform.scale(player_image.subsurface((frames[0]['frame']['x'], frames[0]['frame']['y']), (w, h)),PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[1]['frame']['x'], frames[1]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[2]['frame']['x'], frames[2]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[3]['frame']['x'], frames[3]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE)#.set_colorkey(pygame.Color('white'))
        ]

        frames = player_json['running']['down']
        self.running_down_images = [
            pygame.transform.scale(player_image.subsurface((frames[0]['frame']['x'], frames[0]['frame']['y']), (w, h)),PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[1]['frame']['x'], frames[1]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[2]['frame']['x'], frames[2]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[3]['frame']['x'], frames[3]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE)#.set_colorkey(pygame.Color('white'))
        ]

        frames = player_json['running']['right']
        self.running_right_images = [
            pygame.transform.scale(player_image.subsurface((frames[0]['frame']['x'], frames[0]['frame']['y']), (w, h)),PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[1]['frame']['x'], frames[1]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[2]['frame']['x'], frames[2]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE),#.set_colorkey(pygame.Color('white')),
            pygame.transform.scale(player_image.subsurface((frames[3]['frame']['x'], frames[3]['frame']['y']), (w, h)), PLAYER_SPRITE_SIZE)#.set_colorkey(pygame.Color('white'))
        ]

        # Set spawn sprite
        self.image = self.walking_down_images[0]
        self.rect = self.image.get_rect()
        # Set sprite pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[0]

    def isPokemonAlive(self, idx):
        pokemon = self.pokemon[idx]
        return pokemon.get_dynamic_stat_val('hp') > 0

    # update player sprite 
    def update(self):
        # Add x velocity to x pos
        self.rect.x += self.vel.x
        # Check collision
        self.collide()
        # Add y velocity to y pos
        self.rect.y += self.vel.y
        # Check collision
        self.collide()
        # Iter sprite animation frames
        self.animate()
        # reset velocity value
        self.vel *= 0
        
    def collide(self):
        # moving in y direction
        if self.vel.x == 0 and self.vel.y != 0:
            # find sprites that are colliding
            collision = pygame.sprite.spritecollide(self, self.game.struct_tiles, False)
            encouter_collision = pygame.sprite.spritecollide(self, self.game.encouter_tiles, False)
            # if there are collision, empty list if none
            if collision:
                # check for right
                if self.vel.y > 0:
                    # move player back to orig pos based on colliding sprite
                    self.rect.y = collision[0].rect.top - self.rect.height
                    # camera glitch fix
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += self.vel.y

                    #self.set_route(collision)
                    
                if self.vel.y < 0:
                    # TODO 
                    if collision[0].id == BIG_WOODEN_HOUSE_DOOR_ID:
                        self.game.map.should_transition = True
                    self.rect.y = collision[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += self.vel.y
            elif encouter_collision:
                if random.random() < ENCOUTER_PROB:
                    self.encouter_pokemon = self.game.pokedex.pokemon[random.randint(0, self.game.pokedex.size-1)]
                    # for rn there is only one user pokemon (idx 0)
                    # could be added too
                    if self.isPokemonAlive(0):
                        self.game.battlemenu.infobox.add_sentences('A wild {} has appeared!'.format(self.encouter_pokemon.name.capitalize()))
                        self.game.battlemenu.infobox.add_sentences('What do you want to do?')
                        pygame.mixer.music.stop()
                        self.game.battle_init()
                        self.game.STATE = 4

                    #self.set_route(collision)
        # moving in x direction
        if self.vel.y == 0 and self.vel.x != 0:
            collision = pygame.sprite.spritecollide(self, self.game.struct_tiles, False)
            encouter_collision = pygame.sprite.spritecollide(self, self.game.encouter_tiles, False)
            if collision:
                if self.vel.x > 0:
                    #print('x>0 {}'.format(self.vel.x))
                    self.rect.x = collision[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += self.vel.x

                    #self.set_route(collision)
                if self.vel.x < 0:
                    #print('x<0 {}'.format(self.vel.x))
                    self.rect.x = collision[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += self.vel.x

                    #self.set_route(collision)
            elif encouter_collision:
                if random.random() < ENCOUTER_PROB:
                    self.encouter_pokemon = self.game.pokedex.pokemon[random.randint(0, self.game.pokedex.size-1)]
                    if self.isPokemonAlive(0):
                        self.game.battlemenu.infobox.add_sentences('A wild {} has appeared!'.format(self.encouter_pokemon.name.capitalize()))
                        self.game.battlemenu.infobox.add_sentences('What do you want to do?')
                        pygame.mixer.music.stop()
                        self.game.battle_init()
                        self.game.STATE = 4


    def set_route(self, collision):
        c_x = collision[0].rect.x#+TILE_SIZE
        c_y = collision[0].rect.y#+TILE_SIZE
        #print(collision[0].id)
        if collision[0].id == BIG_WOODEN_HOUSE_DOOR_ID:
            for entry_route in ENTRY_ROUTES:
                e_x = entry_route['check'][0]*TILE_SIZE
                e_y = entry_route['check'][1]*TILE_SIZE
                if collision[0].coord == (e_x, e_y):
                    entry_route['goto'] = True
                    self.game.map.route = entry_route
        elif collision[0].id == CASTLE_DOOR_ID_1 or collision[0].id == CASTLE_DOOR_ID_2:
            route = ENTRY_ROUTES[2]
            route['goto'] = True
            self.game.map.route = route
        elif collision[0].id == HOUSE_EXIT_ID:
            print('Detected?')
            for entry_route in EXIT_ROUTES:
                e_x = entry_route['check'][0]*TILE_SIZE
                e_y = entry_route['check'][1]*TILE_SIZE
                if collision[0].coord == (e_x, e_y):
                    entry_route['goto'] = True
                    self.game.map.route = entry_route


    def animate(self):

        # running
        if abs(self.vel.x) == PLAYER_RUNNING_VEL or abs(self.vel.y) == PLAYER_RUNNING_VEL:
            if self.facing == 'up':
                    self.image = self.running_up_images[math.floor(self.animation_idx)]
                    self.animation_idx += APF
                    if self.animation_idx >= 4:
                        self.animation_idx = 0
            elif self.facing == 'down':
                    self.image = self.running_down_images[math.floor(self.animation_idx)]
                    self.animation_idx += APF
                    if self.animation_idx >= 4:
                        self.animation_idx = 0
            elif self.facing == 'left':
                    self.image = self.running_left_images[math.floor(self.animation_idx)]
                    self.animation_idx += APF
                    if self.animation_idx >= 4:
                        self.animation_idx = 0
            elif self.facing == 'right':
                    self.image = self.running_right_images[math.floor(self.animation_idx)]
                    self.animation_idx += APF
                    if self.animation_idx >= 4:
                        self.animation_idx = 0
        # walking
        else:
            # Check key
            if self.facing == 'up':
                # not moving?
                if self.vel.y == 0:
                    # set static image
                    self.image = self.walking_up_images[0]
                else:
                    # moving, use animation idx
                    self.image = self.walking_up_images[math.floor(self.animation_idx)]
                    # floor(2.3) = 2, floor(2.9) = 2, etc
                    # increment animation idx with APF 
                    self.animation_idx += APF
                    # reset if greater then list len
                    if self.animation_idx >= 4:
                        self.animation_idx = 1
            elif self.facing == 'down':
                if self.vel.y == 0:
                    self.image = self.walking_down_images[0]
                else:
                    self.image = self.walking_down_images[math.floor(self.animation_idx)]
                    self.animation_idx += APF
                    if self.animation_idx >= 4:
                        self.animation_idx = 1
            elif self.facing == 'left':
                if self.vel.x == 0:
                    self.image = self.walking_left_images[0]
                else:
                    self.image = self.walking_left_images[math.floor(self.animation_idx)]
                    self.animation_idx += APF
                    if self.animation_idx >= 4:
                        self.animation_idx = 1
            elif self.facing == 'right':
                if self.vel.x == 0:
                    self.image = self.walking_right_images[0]
                else:
                    self.image = self.walking_right_images[math.floor(self.animation_idx)]
                    self.animation_idx += APF
                    if self.animation_idx >= 4:
                        self.animation_idx = 1
    
    # draw 
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
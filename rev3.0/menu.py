
from consts import *

import pygame
import math
import os
from dirs import BATTLEMENU_DIR, FONTS_DIR, STARTMENU_DIR

from utils import load_image_file, load_json_file

class Menu:

    def __init__(self, game):
        self.game = game

        self.logo = load_image_file(STARTMENU_DIR, 'logo.png')
        self.logo = pygame.transform.scale(self.logo, (SCREEN_W, SCREEN_H//3))
        
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.midtop = (SCREEN_W//2, 0)

        self.text = 'Press SPACE to start'
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, '8-BIT_WONDER.ttf'), 24)

        self.big_font = pygame.font.Font(os.path.join(FONTS_DIR, 'BUBBLE.ttf'), 96)
        self.verison = self.big_font.render('INDIGO', True, pygame.Color(75,0,130))
        self.verison_rect = self.verison.get_rect()
        self.verison_rect.midtop = (self.logo_rect.midbottom[0], self.logo_rect.midbottom[1])

        self.animation_idx = 0
        self.text_animation_idx = 0

        self.cut()

    def cut(self):

        self.pokemon_image = load_image_file(STARTMENU_DIR, 'pikachu.png')
        self.pokemon_rect = self.pokemon_image.get_rect()
        self.pokemon_image_frames = []
        for x in range(0, self.pokemon_rect.w, 500):
            self.pokemon_image_frames.append(pygame.transform.scale(self.pokemon_image.subsurface((x, 0), (500, 633)), (400, 520)))
        self.pokemon_frame = self.pokemon_image_frames[0]
        self.pokemon_frame_rect = self.pokemon_image_frames[0].get_rect()
        self.pokemon_frame_rect.midbottom = (SCREEN_W//2, SCREEN_H-self.font.size('a')[1])

    def update(self):
        self.pokemon_frame = self.pokemon_image_frames[math.floor(self.animation_idx)]
        self.animation_idx += .2
        if self.animation_idx >= len(self.pokemon_image_frames):
            self.animation_idx = 0

        self.display_text = self.text[0:math.floor(self.text_animation_idx)]
        self.rendered_text = self.font.render(self.display_text, True, pygame.Color('black'))
        self.rendered_rect = self.rendered_text.get_rect()
        self.rendered_rect.midbottom = (SCREEN_W//2, SCREEN_H-self.rendered_rect.height)
        self.text_animation_idx += .1
        if self.text_animation_idx >= len(self.text)+1:
            self.text_animation_idx = 0

    def draw(self, screen):
        screen.blit(self.logo, self.logo_rect)
        screen.blit(self.verison, self.verison_rect)
        screen.blit(self.pokemon_frame, self.pokemon_frame_rect)
        screen.blit(self.rendered_text, self.rendered_rect)
        
class BattleMenu:

    def __init__(self):
        
        # 1 = Text, 2 = Action Select, 3 = Move Select
        self.STATE = 1

        self.surf = pygame.Surface(SCREEN_REZ)
        self.surf.fill(pygame.Color('blue'))

        self.JSON_battlemenu = load_json_file(BATTLEMENU_DIR, 'battlemenu.json')

        self.battleboxes_image = load_image_file(BATTLEMENU_DIR, 'battleboxes.png')
        self.textboxes_image = load_image_file(BATTLEMENU_DIR, 'textboxes.png')
        self.battlebuttons_image = load_image_file(BATTLEMENU_DIR, 'battlebuttons.png')

        JSON_image = self.JSON_battlemenu['textbox']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.textbox = self.textboxes_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.textbox = pygame.transform.scale(self.textbox, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.textbox_rect = self.textbox.get_rect()
        self.textbox_rect.midbottom = (SCREEN_W//2, SCREEN_H)
        #self.surf.blit(self.textbox, self.textbox_rect)

        JSON_image = self.JSON_battlemenu['enemybox']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.enemybox = self.battleboxes_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.enemybox = pygame.transform.scale(self.enemybox, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.enemybox_rect = self.enemybox.get_rect()
        self.enemybox_rect.bottomleft = (0, int(SCREEN_H*1/4))
        #self.surf.blit(self.enemybox, self.enemybox_rect)

        JSON_image = self.JSON_battlemenu['playerbox']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.playerbox = self.battleboxes_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.playerbox = pygame.transform.scale(self.playerbox, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.playerbox_rect = self.playerbox.get_rect()
        self.playerbox_rect.bottomright = (SCREEN_W, int(SCREEN_H*3/4))
        #self.surf.blit(self.playerbox, self.playerbox_rect)

        JSON_image = self.JSON_battlemenu['battlebox']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.battlebox = self.battlebuttons_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.battlebox = pygame.transform.scale(self.battlebox, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.battlebox_rect = self.battlebox.get_rect()
        self.battlebox_rect.midbottom = (SCREEN_W//2, SCREEN_H)
        #self.surf.blit(self.battlebox, self.battlebox_rect)

        JSON_image = self.JSON_battlemenu['battleinterface']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.battleinterface = self.battlebuttons_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.battleinterface = pygame.transform.scale(self.battleinterface, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.battleinterface_rect = self.battleinterface.get_rect()
        self.battleinterface_rect.midbottom = (SCREEN_W//2, SCREEN_H)
        #self.surf.blit(self.battleinterface, self.battleinterface_rect)

      

        '''
        #enemy
        self.image = load_image_file(BATTLEMENU_DIR, 'battle2.png')
        self.image = self.image.subsurface((32+260, 28), (120, 32))
        self.image = pygame.transform.scale(self.image, (SCREEN_W//2, 125))
        self.image_rect = self.image.get_rect()

        self.surf.blit(self.image, self.image_rect)

       
        self.image = load_image_file(BATTLEMENU_DIR, 'textboxes.png')
        self.image = self.image.subsurface((1, 0), (250, 46))
        self.image = pygame.transform.scale(self.image, (SCREEN_W, 200))
        self.image_rect = self.image.get_rect()
        self.image_rect.midbottom = (SCREEN_W//2, SCREEN_H)
        self.surf.blit(self.image, self.image_rect)

         #player
        self.image = load_image_file(BATTLEMENU_DIR, 'battle2.png')
        self.image = self.image.subsurface((32+250, 28+32), (120+5, 32+32))
        self.image = pygame.transform.scale(self.image, (SCREEN_W//2, 250))
        self.image_rect = self.image.get_rect()
        self.image_rect.topright = (SCREEN_W, SCREEN_H//4+SCREEN_H//2)
        self.surf.blit(self.image, self.image_rect)
        '''
        #self.surf = pygame.transform.scale(self.surf, (SCREEN_REZ))

    def change_state(self):
        if self.STATE == 3:
            self.STATE = 1
        else:
            self.STATE += 1
    
        self.render_state()

    def render_state(self):
        self.surf.fill(pygame.Color('black'))
        if self.STATE == 1:
            self.surf.blit(self.textbox, self.textbox_rect)
            self.surf.blit(self.playerbox, self.playerbox_rect)
            self.surf.blit(self.enemybox, self.enemybox_rect)
        elif self.STATE == 2:
            self.surf.blit(self.battlebox, self.battlebox_rect)
        elif self.STATE == 3:
            self.surf.blit(self.battleinterface, self.battleinterface_rect)

    def draw(self, screen):
        screen.blit(self.surf, self.surf.get_rect())
        #screen.blit(self.image, self.image.get_rect())
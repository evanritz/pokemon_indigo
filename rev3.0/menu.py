
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
        
        self.surf = pygame.Surface(SCREEN_REZ)
        self.image = load_image_file(BATTLEMENU_DIR, 'battle.png')
        self.image = self.image.subsurface((0, 0), (156, 60))
        self.image = pygame.transform.scale(self.image, (600, 200))
        self.surf.blit(self.image, self.image.get_rect())

        self.image = load_image_file(BATTLEMENU_DIR, 'textboxes.png')
        self.image = self.image.subsurface((0, 0), (251, 46))
        self.image = pygame.transform.scale(self.image, (SCREEN_W, 200))
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (SCREEN_W//2, SCREEN_H//2)
        self.surf.blit(self.image, self.image_rect)

    def draw(self, screen):
        screen.blit(self.surf, self.surf.get_rect())
        #screen.blit(self.image, self.image.get_rect())
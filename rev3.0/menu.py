# menu.py
#
# Holds all game menus 
#
# Written by Evan

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

        self.default_font = pygame.font.Font(os.path.join(FONTS_DIR, 'ARIAL.ttf'), 24)
        self.cr = self.default_font.render('© 2021 Team Best', True, pygame.Color('black'))
        self.cr_rect = self.cr.get_rect()
        self.cr_rect.bottomright = (SCREEN_W, SCREEN_H)

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
        screen.blit(self.cr, self.cr_rect)
        screen.blit(self.logo, self.logo_rect)
        screen.blit(self.verison, self.verison_rect)
        screen.blit(self.pokemon_frame, self.pokemon_frame_rect)
        screen.blit(self.rendered_text, self.rendered_rect)
        
class BattleMenu:

    def __init__(self, game):
        
        self.game = game
        # 1 = Text, 2 = Action Select, 3 = Move Select
        self.STATE = 1
        self.state_changed = True
        self.t0 = pygame.time.get_ticks()
        self.delay = 50

        # For animating state transitions
        self.animate = False

        self.player_pokemon = self.game.player.pokemon[0]
        self.enemy_pokemon = self.game.player.pokemon[0]

        self.name_font = pygame.font.Font(os.path.join(FONTS_DIR, '8-BIT_WONDER.ttf'), 24)
        self.num_font = pygame.font.Font(os.path.join(FONTS_DIR, 'PIXELOID_SANS.ttf'), 24)

        self.surf = pygame.Surface(SCREEN_REZ)
        #self.surf.fill(pygame.Color('blue'))

        self.JSON_battlemenu = load_json_file(BATTLEMENU_DIR, 'battlemenu.json')

        self.battleboxes_image = load_image_file(BATTLEMENU_DIR, 'battleboxes2.png')
        self.textboxes_image = load_image_file(BATTLEMENU_DIR, 'textboxes.png')
        self.battlebuttons_image = load_image_file(BATTLEMENU_DIR, 'battlebuttons.png')
        self.battlebgs_image = load_image_file(BATTLEMENU_DIR, 'battlebgs.png')

        JSON_image = self.JSON_battlemenu['bgs']['grass']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.bg = self.battlebgs_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.bg = pygame.transform.scale(self.bg, (JSON_size['w']*REZ_SCALE, JSON_size['h']*(REZ_SCALE+1)))
        self.bg_rect = self.bg.get_rect()
        self.bg_rect.midbottom = (SCREEN_W//2, 704)

        JSON_image = self.JSON_battlemenu['fgs']['grass']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.fg = self.battlebgs_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.fg = pygame.transform.scale(self.fg, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.fg_rect = self.fg.get_rect()
        self.fg_rect.midbottom = (SCREEN_W//2, 704)

        JSON_image = self.JSON_battlemenu['textbox']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.textbox = self.textboxes_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.textbox = pygame.transform.scale(self.textbox, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.textbox_rect = self.textbox.get_rect()
        self.textbox_rect.midbottom = (SCREEN_W//2, SCREEN_H-8)
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

        JSON_image = self.JSON_battlemenu['boxbars']['greenbar']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.greenbar = self.battleboxes_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.greenbar = pygame.transform.scale(self.greenbar, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.greenbar_rect = self.greenbar.get_rect()
        self.greenbar_rect.topleft = (self.playerbox_rect.center[0]+8, self.playerbox_rect.center[1]-6)

        
       
        JSON_image = self.JSON_battlemenu['battlebox']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.battlebox = self.battlebuttons_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.battlebox = pygame.transform.scale(self.battlebox, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.battlebox_rect = self.battlebox.get_rect()
        self.battlebox_rect.midbottom = (SCREEN_W//2, SCREEN_H*2)
        #self.surf.blit(self.battlebox, self.battlebox_rect)

        JSON_image = self.JSON_battlemenu['battleinterface']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.battleinterface = self.battlebuttons_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.battleinterface = pygame.transform.scale(self.battleinterface, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.battleinterface_rect = self.battleinterface.get_rect()
        self.battleinterface_rect.midbottom = (SCREEN_W//2, SCREEN_H*2)
        #self.surf.blit(self.battleinterface, self.battleinterface_rect)

        
        self.render_player()
        self.render_enemy()
        self.render_state()

    def update(self):
        #print(self.battlebox_rect.center)
        if self.animate:    
            if self.STATE == 2:
                if self.battlebox_rect.midbottom > (SCREEN_W//2, SCREEN_H):
                    self.t1 = pygame.time.get_ticks()
                    if self.t1-self.t0 >= self.delay:
                        self.t1 = self.t0
                        self.battlebox_rect.midbottom = (SCREEN_W//2, self.battlebox_rect.midbottom[1]-20)
                else:
                    self.animate = False
            elif self.STATE == 1:
                if self.battleinterface_rect.midbottom < (SCREEN_W//2, SCREEN_H*2):
                    self.t1 = pygame.time.get_ticks()
                    if self.t1-self.t0 >= self.delay:
                        self.t1 = self.t0
                        self.battleinterface_rect.midbottom = (SCREEN_W//2, self.battleinterface_rect.midbottom[1]+20)
                else:
                    self.animate = False

            self.render_state()
            self.render_player()
            self.render_enemy()

    def render_player(self):
        # slash
        self.slash = self.num_font.render('/', True, pygame.Color((46, 46, 46)))
        self.slash_rect = self.slash.get_rect()
        self.slash_rect.topleft = (892, 616)

        # top frac
        pokemon_hp = self.player_pokemon.get_dynamic_stat_val('hp')
        self.top_frac = self.num_font.render(str(pokemon_hp), True, pygame.Color((46, 46, 46)))
        self.top_frac_rect = self.top_frac.get_rect()
        self.top_frac_rect.topright = (888, 616)

        # bot frac
        pokemon_max_hp = self.player_pokemon.get_static_stat_val('hp')
        self.bot_frac = self.num_font.render(str(pokemon_max_hp), True, pygame.Color((46, 46, 46)))
        self.bot_frac_rect = self.bot_frac.get_rect()
        self.bot_frac_rect.topleft = (916, 616)

        # level
        pokemon_level = self.player_pokemon.get_dynamic_stat_val('level')
        self.level = self.num_font.render('Lv{}'.format(pokemon_level), True, pygame.Color((46, 46, 46)))
        self.level_rect = self.level.get_rect()
        self.level_rect.topleft = (884, 540)

        # name
        pokemon_name = self.player_pokemon.name
        self.name = self.name_font.render(pokemon_name, True, pygame.Color((46, 46, 46)))
        self.name_rect = self.name.get_rect()
        self.name_rect.bottomleft = (600, 564)

    def render_enemy(self):

        # level
        pokemon_level = self.enemy_pokemon.get_dynamic_stat_val('level')
        self.enemy_level = self.num_font.render('Lv{}'.format(pokemon_level), True, pygame.Color((46, 46, 46)))
        self.enemy_level_rect = self.level.get_rect()
        self.enemy_level_rect.topleft = (292, 136)
        
        # name
        pokemon_name = self.enemy_pokemon.name
        self.enemy_name = self.name_font.render(pokemon_name, True, pygame.Color((46, 46, 46)))
        self.enemy_name_rect = self.enemy_name.get_rect()
        self.enemy_name_rect.bottomleft = (12, 160)

    def change_state(self):
        
        self.state_changed = True
        
        if self.STATE == 3:
            self.STATE = 1
        else:
            self.STATE += 1
    
        if self.STATE == 1:
            self.render_player()
            self.render_enemy()
            self.surf.fill(pygame.Color('black'))

        elif self.STATE == 2:
            #print(self.battlebox_rect.midbottom)
            self.surf.fill(pygame.Color('black'))
            self.battlebox_rect.midbottom = (SCREEN_W//2, SCREEN_H*2)
        
        elif self.STATE == 3:
            self.surf.fill(pygame.Color('black'))
            self.battleinterface_rect.midbottom = (SCREEN_W//2, SCREEN_H)

        self.render_state()

    def render_state(self):
        #self.surf.fill(pygame.Color('black'))
        if self.STATE == 1:
            self.surf.fill(pygame.Color('black'))
            self.surf.blit(self.bg, self.bg_rect)
            self.surf.blit(self.fg, self.fg_rect)
            self.surf.blit(self.textbox, self.textbox_rect)
            self.surf.blit(self.playerbox, self.playerbox_rect)
            self.surf.blit(self.enemybox, self.enemybox_rect)
            self.surf.blit(self.greenbar, self.greenbar_rect)
            self.surf.blit(self.slash, self.slash_rect)
            self.surf.blit(self.top_frac, self.top_frac_rect)
            self.surf.blit(self.bot_frac, self.bot_frac_rect)
            self.surf.blit(self.level, self.level_rect)
            self.surf.blit(self.enemy_level, self.enemy_level_rect)
            self.surf.blit(self.name, self.name_rect)
            self.surf.blit(self.enemy_name, self.enemy_name_rect)
            self.surf.blit(self.battleinterface, self.battleinterface_rect)

            
            #pygame.image.save(self.surf, 'screen.png')
        elif self.STATE == 2:
            self.surf.fill(pygame.Color('black'))
            self.surf.blit(self.bg, self.bg_rect)
            self.surf.blit(self.fg, self.fg_rect)
            self.surf.blit(self.textbox, self.textbox_rect)
            self.surf.blit(self.playerbox, self.playerbox_rect)
            self.surf.blit(self.enemybox, self.enemybox_rect)
            self.surf.blit(self.greenbar, self.greenbar_rect)
            self.surf.blit(self.slash, self.slash_rect)
            self.surf.blit(self.top_frac, self.top_frac_rect)
            self.surf.blit(self.bot_frac, self.bot_frac_rect)
            self.surf.blit(self.level, self.level_rect)
            self.surf.blit(self.enemy_level, self.enemy_level_rect)
            self.surf.blit(self.name, self.name_rect)
            self.surf.blit(self.enemy_name, self.enemy_name_rect)
            self.surf.blit(self.battlebox, self.battlebox_rect)
        elif self.STATE == 3:
            self.surf.fill(pygame.Color('black'))
            self.surf.blit(self.bg, self.bg_rect)
            self.surf.blit(self.fg, self.fg_rect)
            self.surf.blit(self.textbox, self.textbox_rect)
            self.surf.blit(self.playerbox, self.playerbox_rect)
            self.surf.blit(self.enemybox, self.enemybox_rect)
            self.surf.blit(self.battleinterface, self.battleinterface_rect)

    def draw(self, screen):
        #self.surf.blit(self.battlebox, self.battlebox_rect)
        screen.blit(self.surf, self.surf.get_rect())
        #screen.blit(self.image, self.image.get_rect())

class TextBox:
    def __init__(self):
        self.sentences = []

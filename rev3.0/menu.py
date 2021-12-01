# menu.py
#
# Holds all game menus 
#
# Written by Evan

from consts import *

import random
import textwrap
import pygame
import math
import copy
import os


from dirs import BATTLEMENU_DIR, FONTS_DIR, STARTMENU_DIR, POKEMON_DIR, SPRITESHEETS_DIR

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
        self.PREV_STATE = self.STATE

        self.state_changed = True
        self.t0 = pygame.time.get_ticks()
        self.delay = 25
        self.pokemon_delay = 50

        # For animating state transitions
        self.animate = False
        # For animating init transitions
        self.animate_init = True
        self.animate_idx = 0

        self.animate_pokemon_idx = 0#[-1, 0, 1]
        self.player_sprite_dy = 1
        self.enemy_sprite_dy = -1
        self.player_sprite_bound = True
        self.enemy_sprite_bound = True

        self.player_pokemon = self.game.player.pokemon[0]
        #self.player_pokemon.set_dynamic_stat_val('hp', 30)
        #self.enemy_pokemon = copy.deepcopy(self.game.player.encouter_pokemon)#self.game.pokedex.pokemon[45]
        #self.enemy_pokemon.set_dynamic_stat_val('hp', 1)

        self.player_pokemon_sprite = load_image_file(POKEMON_DIR, self.player_pokemon.sprites['back'])
        self.player_pokemon_sprite = pygame.transform.scale(self.player_pokemon_sprite, (96*(REZ_SCALE+1), 96*(REZ_SCALE+1)))
        self.player_pokemon_sprite_rect = self.player_pokemon_sprite.get_rect()
        self.player_pokemon_sprite_rect.center = (256, 615)
        
        #self.enemy_pokemon_sprite = load_image_file(POKEMON_DIR, self.enemy_pokemon.sprites['front'])
        #self.enemy_pokemon_sprite = pygame.transform.scale(self.enemy_pokemon_sprite, (96*REZ_SCALE, 96*REZ_SCALE))
        #self.enemy_pokemon_sprite_rect = self.enemy_pokemon_sprite.get_rect()
        #self.enemy_pokemon_sprite_rect.midbottom = (768, 470+96+32)

        self.player_battle_image = load_image_file(SPRITESHEETS_DIR, 'player_battle.png')
        self.player_battle_frames = []
        for x in range(0, 1024, 128):
            self.player_battle_frames.append(pygame.transform.scale(self.player_battle_image.subsurface((x, 0), (128, 128)), (128*2, 128*2)))
        self.player_battle_frame = self.player_battle_frames[0]
        self.player_battle_frame_rect = self.player_battle_frame.get_rect()
        self.player_battle_frame_rect.midbottom = (256, 704)

        self.black_bg = pygame.Surface((SCREEN_W, 192))
        self.black_bg_rect = self.black_bg.get_rect()
        self.black_bg_rect.topleft = (0, 704)

        self.name_font = pygame.font.Font(os.path.join(FONTS_DIR, '8-BIT_WONDER.ttf'), 24)
        self.num_font = pygame.font.Font(os.path.join(FONTS_DIR, 'PIXELOID_SANS.ttf'), 24)

        self.move_font = pygame.font.Font(os.path.join(FONTS_DIR, 'PIXELOID_SANS.ttf'), 36)
        self.move_pp_font = pygame.font.Font(os.path.join(FONTS_DIR, '8-BIT_WONDER.ttf'), 36)

        self.infobox = InfoBox()
        self.infobox_lines = []
        
        #self.action_selector = ActionSelector()
        self.selector = []
        self.selected = 'NONE'
        self.selected_move = None

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

        self.playerbar = self.greenbar.copy()
        self.playerbar_rect = self.greenbar_rect.copy()
        self.playerbar_rect.topleft = (self.playerbox_rect.center[0]+8, self.playerbox_rect.center[1]-6)

        self.enemybar = self.greenbar.copy()
        self.enemybar_rect = self.greenbar_rect.copy()
        self.enemybar_rect.topleft = (self.enemybox_rect.center[0]-40, self.enemybox_rect.center[1]+16)
       
        JSON_image = self.JSON_battlemenu['battlebox']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.battlebox = self.battlebuttons_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.battlebox = pygame.transform.scale(self.battlebox, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.battlebox_rect = self.battlebox.get_rect()
        self.battlebox_rect.midbottom = (SCREEN_W//2, SCREEN_H*2)
        #self.surf.blit(self.battlebox, self.battlebox_rect)

        JSON_image = self.JSON_battlemenu['battleboxselectors']['big']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.battlebox_bigselect = self.battlebuttons_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.battlebox_bigselect = pygame.transform.scale(self.battlebox_bigselect, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.battlebox_bigselect.set_colorkey((192, 192, 192))
        self.battlebox_bigselect_rect = self.battlebox_bigselect.get_rect()
        
        self.battlebox_ATTACK = self.battlebox_bigselect_rect.copy()
        self.battlebox_ATTACK.center = (511, 408)

        JSON_image = self.JSON_battlemenu['battleboxselectors']['small']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.battlebox_smallselect = self.battlebuttons_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.battlebox_smallselect = pygame.transform.scale(self.battlebox_smallselect, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.battlebox_smallselect.set_colorkey((192, 192, 192))
        self.battlebox_smallselect_rect = self.battlebox_smallselect.get_rect()
        
        self.battlebox_BAG = self.battlebox_smallselect_rect.copy()
        self.battlebox_BAG.center = (160, 756)
        self.battlebox_RUN = self.battlebox_smallselect_rect.copy()
        self.battlebox_RUN.center = (512, 788)
        self.battlebox_POKEMON = self.battlebox_smallselect_rect.copy()
        self.battlebox_POKEMON.center = (864, 756)

        JSON_image = self.JSON_battlemenu['battleinterface']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.battleinterface = self.battlebuttons_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.battleinterface = pygame.transform.scale(self.battleinterface, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.battleinterface_rect = self.battleinterface.get_rect()
        self.battleinterface_rect.midbottom = (SCREEN_W//2, SCREEN_H*2)

        JSON_image = self.JSON_battlemenu['battleboxselectors']['wide']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.battleinterface_wideselect = self.battlebuttons_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.battleinterface_wideselect = pygame.transform.scale(self.battleinterface_wideselect, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.battleinterface_wideselect.set_colorkey((192, 192, 192))
        self.battleinterface_wideselect_rect = self.battleinterface_wideselect.get_rect()

        self.battleinterface_CANCEL = self.battleinterface_wideselect_rect.copy()
        self.battleinterface_CANCEL.topleft = (36, 708)

        JSON_image = self.JSON_battlemenu['battleboxselectors']['medium']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.battleinterface_mediumselect = self.battlebuttons_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.battleinterface_mediumselect = pygame.transform.scale(self.battleinterface_mediumselect, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.battleinterface_mediumselect.set_colorkey((192, 192, 192))
        self.battleinterface_mediumselect_rect = self.battleinterface_mediumselect.get_rect()
        #self.battleinterface_CANCEL.center = 11

        self.battleinterface_MOVE0 = self.battleinterface_mediumselect_rect.copy()
        self.battleinterface_MOVE0.topleft = (4, 184)#(256, 294)#
        self.battleinterface_MOVE1 = self.battleinterface_mediumselect_rect.copy()
        self.battleinterface_MOVE1.topleft = (516, 184)
        self.battleinterface_MOVE2 = self.battleinterface_mediumselect_rect.copy()
        self.battleinterface_MOVE2.topleft = (4, 432)
        self.battleinterface_MOVE3 = self.battleinterface_mediumselect_rect.copy()
        self.battleinterface_MOVE3.topleft = (516, 432)

        # fix for json as I dont want to have to change to a JSON arr
        # create arr of all types and grab from JSON using for loop
        self.types = [
            'ground', 'water', 'ghost', 'bug',
            'fighting', 'psychic', 'grass', 'dark',
            'normal', 'poison', 'electric', 'unknown',
            'steel', 'rock', 'dragon', 'flying',
            'fire', 'ice', 'blank'
        ]

        self.battleinterface_TYPE0_rect = self.battleinterface_MOVE0.copy()
        self.battleinterface_TYPE0_rect.center = (264, 302)
        self.battleinterface_TYPE1_rect = self.battleinterface_MOVE1.copy()
        self.battleinterface_TYPE1_rect.center = (776, 302)
        self.battleinterface_TYPE2_rect = self.battleinterface_MOVE2.copy()
        self.battleinterface_TYPE2_rect.center = (264, 550)
        self.battleinterface_TYPE3_rect = self.battleinterface_MOVE3.copy()
        self.battleinterface_TYPE3_rect.center = (776, 550)

        self.type_surfs = {}

        for type in self.types:
            JSON_image = self.JSON_battlemenu['battleinterfacetypes'][type]
            JSON_pos = JSON_image['pos']
            JSON_size = JSON_image['size']
            battleinterface_TYPE = self.battlebuttons_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
            battleinterface_TYPE = pygame.transform.scale(battleinterface_TYPE, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
            self.type_surfs.update({type: battleinterface_TYPE})
            
        self.battleinterface_SURF0 = self.type_surfs['unknown']
        self.battleinterface_SURF1 = self.type_surfs['unknown']
        self.battleinterface_SURF2 = self.type_surfs['unknown']
        self.battleinterface_SURF3 = self.type_surfs['unknown']

        # Move name for moves
        self.battleinterface_MOVENAME0 = []
        self.battleinterface_MOVENAME1 = []
        self.battleinterface_MOVENAME2 = []
        self.battleinterface_MOVENAME3 = []

        # PP for all moves
        self.battleinterface_MOVEPP0 = []
        self.battleinterface_MOVEPP1 = []
        self.battleinterface_MOVEPP2 = []
        self.battleinterface_MOVEPP3 = []

        JSON_image = self.JSON_battlemenu['battleinterfacetypes']['ghost']
        JSON_pos = JSON_image['pos']
        JSON_size = JSON_image['size']
        self.battleinterface_GHOST = self.battlebuttons_image.subsurface((JSON_pos['x'], JSON_pos['y']), (JSON_size['w'], JSON_size['h']))
        self.battleinterface_GHOST = pygame.transform.scale(self.battleinterface_GHOST, (JSON_size['w']*REZ_SCALE, JSON_size['h']*REZ_SCALE))
        self.battleinterface_GHOST_rect = self.battleinterface_MOVE0.copy()
        self.battleinterface_GHOST_rect.center = (260, 294)


        #self.surf.blit(self.battleinterface, self.battleinterface_rect)

        #self.render_selection()
        #self.render_player()
        #self.render_enemy()
        #self.render_textbox()
        #self.render_state()
        
    def check_mouse(self, mx, my, left):
        if self.STATE == 2 and not self.animate:
            if self.battlebox_ATTACK.collidepoint(mx, my):
                self.selector = [self.battlebox_bigselect, self.battlebox_ATTACK]
                if left:
                    self.selected = 'ATTACK'
            elif self.battlebox_BAG.collidepoint(mx, my):
                self.selector = [self.battlebox_smallselect, self.battlebox_BAG]
                if left:
                    self.selected = 'BAG'
            elif self.battlebox_RUN.collidepoint(mx, my):
                self.selector = [self.battlebox_smallselect, self.battlebox_RUN]
                if left:
                    self.selected = 'RUN'
            elif self.battlebox_POKEMON.collidepoint(mx, my):
                self.selector = [self.battlebox_smallselect, self.battlebox_POKEMON]
                if left:
                    self.selected = 'POKEMON'
            else:
                self.selector = []
                self.selected = 'NONE'

            #self.game.mouse.reset_buttons()

        elif self.STATE == 3 and not self.animate:
            moves = self.player_pokemon.get_dynamic_moves()
            if self.battleinterface_CANCEL.collidepoint(mx, my):
                self.selector = [self.battleinterface_wideselect, self.battleinterface_CANCEL]
                if left:
                    self.selected = 'CANCEL'
            elif self.battleinterface_MOVE0.collidepoint(mx, my):
                self.selector = [self.battleinterface_mediumselect, self.battleinterface_MOVE0]
                if left:
                    self.selected = 'MOVE0'
                    self.selected_move = moves[0]
            elif self.battleinterface_MOVE1.collidepoint(mx, my):
                self.selector = [self.battleinterface_mediumselect, self.battleinterface_MOVE1]
                if left:
                    self.selected = 'MOVE1'
                    self.selected_move = moves[1]
            elif self.battleinterface_MOVE2.collidepoint(mx, my):
                self.selector = [self.battleinterface_mediumselect, self.battleinterface_MOVE2]
                if left:
                    self.selected = 'MOVE2'
                    self.selected_move = moves[2]
            elif self.battleinterface_MOVE3.collidepoint(mx, my):
                self.selector = [self.battleinterface_mediumselect, self.battleinterface_MOVE3]
                if left:
                    self.selected = 'MOVE3'
                    self.selected_move = moves[3]
            else:
                self.selector = []
                self.selected = 'NONE'

        print(mx, my, left, self.selected)

    def reset(self):
        self.STATE = 1
        self.animate_init = True
        self.selector = []
        self.animate_idx = 0
        self.player_battle_frame_rect.midbottom = (256, 704)
        self.infobox_lines = []
        self.infobox.lines = []
        self.player_sprite_dy = 1
        self.enemy_sprite_dy = -1
        self.player_sprite_bound = True
        self.enemy_sprite_bound = True

        #self.infobox.sentences = []
        
        #self.enemy_pokemon = None
        

    def update_state(self):
        
        #print(self.selected, self.game.mouse.LEFT)

        if self.STATE == 1:
            
            # if something 
            self.battlebox_rect.midbottom = (SCREEN_W//2, SCREEN_H*2)
            #print(self.infobox.sentences, (not self.infobox.sentences))
            self.render_player()
            self.render_enemy()
            self.render_textbox()
            #if self.animate_init:
            #    if self.player_pokemon.get_dynamic_stat_val('hp') <= 0:
            #        self.game.STATE = 3
            #        self.reset()

            if not self.infobox.sentences and self.infobox.sentence == None:
                
                if self.player_pokemon.get_dynamic_stat_val('hp') <= 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('sounds/pallet_town.WAV')
                    pygame.mixer.music.play(-1)
                    self.game.STATE = 3
                    #self.infobox.add_sentences('test1')
                    self.reset()
                elif self.enemy_pokemon.get_dynamic_stat_val('hp') <= 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('sounds/pallet_town.WAV')
                    pygame.mixer.music.play(-1)
                    self.game.STATE = 3
                    #self.infobox.add_sentences('test1')
                    self.reset()
                else:
                    self.STATE = 2 
                    self.selector = []
                    self.animate = True

           

        elif self.STATE == 2:

            self.render_selection()
            
            if self.selected == 'ATTACK':
                self.STATE = 3
                self.selector = []
                #self.wait = True
            elif self.selected == 'RUN':
                pygame.mixer.music.stop()
                pygame.mixer.music.load('sounds/pallet_town.WAV')
                pygame.mixer.music.play(-1)
                self.game.STATE = 3
                self.reset()

            self.selected = 'NONE'
            #self.game.mouse.reset_buttons()

        elif self.STATE == 3:

            self.battleinterface_rect.midbottom = (SCREEN_W//2, SCREEN_H)
            self.battleinterface_MOVE0.topleft = (4, 184)
            self.battleinterface_MOVE1.topleft = (516, 184)
            self.battleinterface_MOVE2.topleft = (4, 432)
            self.battleinterface_MOVE3.topleft = (516, 432)
            self.render_selection()

            if self.selected == 'CANCEL':
                self.STATE = 2
            elif self.selected in ['MOVE0', 'MOVE1', 'MOVE2', 'MOVE3']:
                self.STATE = 1
                self.animate = True
                self.selector = []
                #self.infobox.lines = []
                self.infobox_lines = []
                self.calc_selected_move()
                self.infobox.increment_sentences()
                #self.infobox.add_sentences('memes')

            self.selected = 'NONE'
            #self.game.mouse.reset_buttons()

        #print(self.STATE, self.PREV_STATE)
        #self.PREV_STATE = self.STATE

    def update(self):
        
        if self.STATE == 1:
            
            self.t1 = pygame.time.get_ticks()
            if self.t1-self.t0 >= self.pokemon_delay:
                self.t1 = self.t0
                p_x, p_y = self.player_pokemon_sprite_rect.center
                self.player_pokemon_sprite_rect.center = (p_x, p_y+self.player_sprite_dy)
        
                if self.player_sprite_bound:
                    if self.player_pokemon_sprite_rect.center >= (256, 630):
                        self.player_sprite_dy = -self.player_sprite_dy
                    elif self.player_pokemon_sprite_rect.center <= (256, 600):
                        self.player_sprite_dy = -self.player_sprite_dy

                e_x, e_y = self.enemy_pokemon_sprite_rect.midbottom
                self.enemy_pokemon_sprite_rect.midbottom = (e_x, e_y+self.enemy_sprite_dy)

                if self.enemy_sprite_bound:
                    if self.enemy_pokemon_sprite_rect.midbottom >= (768, 600):
                        self.enemy_sprite_dy = -self.enemy_sprite_dy
                    elif self.enemy_pokemon_sprite_rect.midbottom <= (768, 570):
                        self.enemy_sprite_dy = -self.enemy_sprite_dy

                if self.enemy_pokemon_sprite_rect.topleft[1] > SCREEN_H:
                    self.enemy_sprite_dy = 0

                if self.player_pokemon_sprite_rect.topleft[1] > SCREEN_H:
                    self.player_sprite_dy = 0


                print(p_x, p_y)
                print(e_x, e_y)

        if self.animate_init:
            if self.STATE == 1:
                self.player_battle_frame = self.player_battle_frames[math.floor(self.animate_idx)]
                self.animate_idx += .05
                
                x, y = self.player_battle_frame_rect.midbottom
                self.player_battle_frame_rect.midbottom = (x-4, y)
                
                if self.animate_idx >= len(self.player_battle_frames)-2:
                    self.player_battle_frame_rect.midbottom = (256, 704)

                if self.animate_idx >= len(self.player_battle_frames):
                    self.animate_init = False
                    self.animate_idx = 0

        elif self.animate:   
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
       


   
            
        self.update_state()
        self.render_state()
            
            

    def render_player(self):
        # slash
        self.slash = self.num_font.render('/', True, pygame.Color((46, 46, 46)))
        self.slash_rect = self.slash.get_rect()
        self.slash_rect.topleft = (892, 616)

        # top frac
        pokemon_hp = self.player_pokemon.get_dynamic_stat_val('hp')
        
        if pokemon_hp < 0:
            pokemon_hp = 0

        self.top_frac = self.num_font.render(str(pokemon_hp), True, pygame.Color((46, 46, 46)))
        self.top_frac_rect = self.top_frac.get_rect()
        self.top_frac_rect.topright = (888, 616)

        # bot frac
        pokemon_max_hp = self.player_pokemon.get_static_stat_val('hp')
        self.bot_frac = self.num_font.render(str(pokemon_max_hp), True, pygame.Color((46, 46, 46)))
        self.bot_frac_rect = self.bot_frac.get_rect()
        self.bot_frac_rect.topleft = (916, 616)

        # health bar
        ratio = pokemon_hp/pokemon_max_hp
        scaled_w = int(ratio*self.greenbar_rect.width)
        self.playerbar = self.greenbar.subsurface((0, 0), (scaled_w, self.greenbar_rect.height))

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
        print(self.enemy_pokemon.dynamic_stats)
        pokemon_level = self.enemy_pokemon.get_dynamic_stat_val('level')
        self.enemy_level = self.num_font.render('Lv{}'.format(pokemon_level), True, pygame.Color((46, 46, 46)))
        self.enemy_level_rect = self.enemy_level.get_rect()
        self.enemy_level_rect.topleft = (292, 136)
        
        # name
        pokemon_name = self.enemy_pokemon.name
        self.enemy_name = self.name_font.render(pokemon_name, True, pygame.Color((46, 46, 46)))
        self.enemy_name_rect = self.enemy_name.get_rect()
        self.enemy_name_rect.bottomleft = (12, 160)

        # health bar
        pokemon_max_hp = self.enemy_pokemon.get_static_stat_val('hp')
        pokemon_hp = self.enemy_pokemon.get_dynamic_stat_val('hp')
        ratio = pokemon_hp/pokemon_max_hp
        scaled_w = int(ratio*self.greenbar_rect.width)
        self.enemybar = self.greenbar.subsurface((0, 0), (scaled_w, self.greenbar_rect.height))

        #self.enemy_pokemon = copy.deepcopy(pokemon)#self.game.pokedex.pokemon[45]

    def set_enemy(self, pokemon):
        self.enemy_pokemon = copy.deepcopy(pokemon)#self.game.pokedex.pokemon[45]
        self.enemy_pokemon_sprite = load_image_file(POKEMON_DIR, self.enemy_pokemon.sprites['front'])
        self.enemy_pokemon_sprite = pygame.transform.scale(self.enemy_pokemon_sprite, (96*REZ_SCALE, 96*REZ_SCALE))
        self.enemy_pokemon_sprite_rect = self.enemy_pokemon_sprite.get_rect()
        self.enemy_pokemon_sprite_rect.midbottom = (768, 585)

    def render_textbox(self):

        lines = self.infobox.lines
        
        y_inc = self.name_font.render('A', True, pygame.Color((46, 46, 46))).get_rect().height
        for y_mult, line in enumerate(lines):
            
            idx = y_mult
            y = y_inc*y_mult + self.textbox_rect.y + IBL_Y_OFFSET
            x = self.textbox_rect.x + 2*IBL_X_OFFSET
            rendered_line = self.num_font.render(line, True, pygame.Color((46, 46, 46)))
            rendered_line_rect = rendered_line.get_rect()
            rendered_line_rect.topleft = (x, y)
            self.infobox_lines.insert(idx, [rendered_line, rendered_line_rect])

            
    def render_move_details(self, move, idx):
            
            name = move['name'].capitalize()
            pp = move['pp']

            rendered_name = self.move_font.render(name, True, pygame.Color((46, 46, 46)))
            rendered_name_rect = rendered_name.get_rect()

            #rendered_pp = self.num_font.render(str(pp), True, pygame.Color((46, 46, 46)))
            #rendered_pp_rect = rendered_pp.get_rect()

            if idx == 0:
                rendered_name_rect.midtop = (256, 232)
                self.battleinterface_MOVENAME0 = [rendered_name, rendered_name_rect]
            elif idx == 1:
                rendered_name_rect.midtop = (768, 232)
                self.battleinterface_MOVENAME1 = [rendered_name, rendered_name_rect]
            elif idx == 2:
                rendered_name_rect.midtop = (256, 480)
                self.battleinterface_MOVENAME2 = [rendered_name, rendered_name_rect]
            elif idx == 3:
                rendered_name_rect.midtop = (768, 480)
                self.battleinterface_MOVENAME3 = [rendered_name, rendered_name_rect]

    def render_selection(self):
       move_names = self.player_pokemon.get_static_moves()
       for idx, move_name in enumerate(move_names):
            print(idx, move_name)
            move = self.player_pokemon.get_dynamic_move_details(move_name)
            static_move = self.player_pokemon.get_static_move_details(move_name)
            print(move, static_move)

            type = move['type']

            self.render_move_details(move, idx)

            rendered_pp_text = self.move_font.render('PP', True, pygame.Color((46, 46, 46)))
            rendered_pp_text_rect = rendered_pp_text.get_rect()
            rendered_pp_text_rect.topleft = (220, 124)

            pp = move['pp']
            rendered_pp = self.move_font.render(str(pp), True, pygame.Color((46, 46, 46)))
            rendered_pp_rect = rendered_pp.get_rect()
            rendered_pp_rect.topleft = (rendered_pp_text_rect.topright[0] + 4, rendered_pp_text_rect.topright[1])

            rendered_slash = self.move_font.render('/', True, pygame.Color((46, 46, 46)))
            rendered_slash_rect = rendered_slash.get_rect()
            rendered_slash_rect.topleft = (rendered_pp_rect.topright[0] + 4, rendered_pp_rect.topright[1])

            max_pp = static_move['pp']
            rendered_max_pp = self.move_font.render(str(max_pp), True, pygame.Color((46, 46, 46)))
            rendered_max_pp_rect = rendered_max_pp.get_rect()
            rendered_max_pp_rect.topleft = (rendered_slash_rect.topright[0] + 4, rendered_slash_rect.topright[1])

            if idx == 0:
                self.battleinterface_SURF0 = self.type_surfs[type].copy()
                self.battleinterface_SURF0.blit(rendered_pp_text, rendered_pp_text_rect)
                self.battleinterface_SURF0.blit(rendered_pp, rendered_pp_rect)
                self.battleinterface_SURF0.blit(rendered_slash, rendered_slash_rect)
                self.battleinterface_SURF0.blit(rendered_max_pp, rendered_max_pp_rect)
            elif idx == 1:
                self.battleinterface_SURF1 = self.type_surfs[type].copy()
                self.battleinterface_SURF1.blit(rendered_pp_text, rendered_pp_text_rect)
                self.battleinterface_SURF1.blit(rendered_pp, rendered_pp_rect)
                self.battleinterface_SURF1.blit(rendered_slash, rendered_slash_rect)
                self.battleinterface_SURF1.blit(rendered_max_pp, rendered_max_pp_rect)
                
            elif idx == 2:
                self.battleinterface_SURF2 = self.type_surfs[type].copy()
                self.battleinterface_SURF2.blit(rendered_pp_text, rendered_pp_text_rect)
                self.battleinterface_SURF2.blit(rendered_pp, rendered_pp_rect)
                self.battleinterface_SURF2.blit(rendered_slash, rendered_slash_rect)
                self.battleinterface_SURF2.blit(rendered_max_pp, rendered_max_pp_rect)
                
            elif idx == 3:
                self.battleinterface_SURF3 = self.type_surfs[type].copy()
                self.battleinterface_SURF3.blit(rendered_pp_text, rendered_pp_text_rect)
                self.battleinterface_SURF3.blit(rendered_pp, rendered_pp_rect)
                self.battleinterface_SURF3.blit(rendered_slash, rendered_slash_rect)
                self.battleinterface_SURF3.blit(rendered_max_pp, rendered_max_pp_rect)
                

    def calc_selected_move(self):
        
        # get all vars
        p_move = self.player_pokemon.get_dynamic_move_details(self.selected_move)
        p_type = p_move['type']
        p_power = p_move['power']
        p_pp = p_move['pp']

        p_hp = self.player_pokemon.get_dynamic_stat_val('hp')
        p_level = self.player_pokemon.get_dynamic_stat_val('level')

        p_attack = self.player_pokemon.get_dynamic_stat_val('attack')
        p_defense = self.player_pokemon.get_dynamic_stat_val('defense')

        p_special_attack = self.player_pokemon.get_dynamic_stat_val('special-attack')
        p_special_defense = self.player_pokemon.get_dynamic_stat_val('special-defense')

        p_speed = self.player_pokemon.get_dynamic_stat_val('speed')

        e_move_names = self.enemy_pokemon.get_dynamic_moves()
        e_move = self.enemy_pokemon.get_dynamic_move_details(e_move_names[random.randint(0, 3)])
        e_type = e_move['type']
        e_power = e_move['power']
        e_pp = e_move['pp']

        e_hp = self.enemy_pokemon.get_dynamic_stat_val('hp')
        e_level = self.enemy_pokemon.get_dynamic_stat_val('level')

        e_attack = self.enemy_pokemon.get_dynamic_stat_val('attack')
        e_defense = self.enemy_pokemon.get_dynamic_stat_val('defense')

        e_special_attack = self.enemy_pokemon.get_dynamic_stat_val('special-attack')
        e_special_defense = self.enemy_pokemon.get_dynamic_stat_val('special-defense')

        e_speed = self.enemy_pokemon.get_dynamic_stat_val('speed')

        type_int = 1
        
        
        
        
        self.infobox.add_sentences('{} used {}'.format(self.player_pokemon.name.capitalize(), p_move['name'].upper()))
        if e_power != None:
            p_damge_hp = int(((((2*e_level)/5 + 2)*e_power*e_attack/p_defense)/50 + 2)*type_int)
            p_hp -= p_damge_hp
            self.player_pokemon.set_dynamic_stat_val('hp', p_hp)
            self.infobox.add_sentences('{} did {} damage to {}!'.format(self.enemy_pokemon.name.capitalize(), p_damge_hp, self.player_pokemon.name.capitalize()))
            
        if e_hp > 0:
            self.infobox.add_sentences('{} used {}'.format(self.enemy_pokemon.name.capitalize(), e_move['name'].upper()))
            if p_power != None:
                e_damge_hp = int(((((2*p_level)/5 + 2)*p_power*p_attack/e_defense)/50 + 2)*type_int)
                e_hp -= e_damge_hp
                self.enemy_pokemon.set_dynamic_stat_val('hp', e_hp)
                self.infobox.add_sentences('{} did {} damage to {}!'.format(self.player_pokemon.name.capitalize(), e_damge_hp, self.enemy_pokemon.name.capitalize()))

        if p_hp <= 0:
                self.infobox.add_sentences('{} fainted!'.format(self.player_pokemon.name.capitalize()))
                self.player_sprite_bound = False
                self.player_sprite_dy = 15
        if e_hp <= 0:
                self.infobox.add_sentences('{} fainted!'.format(self.enemy_pokemon.name.capitalize()))
                self.enemy_sprite_bound = False
                self.enemy_sprite_dy = 15
    def render_state(self):
        #self.surf.fill(pygame.Color('black'))
        print(self.STATE)
        print(self.infobox.sentences)
        if self.STATE == 1:
            self.surf.fill(pygame.Color('black'))
            self.surf.blit(self.bg, self.bg_rect)        
            self.surf.blit(self.fg, self.fg_rect)

            if not self.animate_init:
                self.surf.blit(self.player_pokemon_sprite, self.player_pokemon_sprite_rect)
            else:
                self.surf.blit(self.player_battle_frame, self.player_battle_frame_rect)

            self.surf.blit(self.black_bg, self.black_bg_rect)

            self.surf.blit(self.textbox, self.textbox_rect)

            for line in self.infobox_lines:
                self.surf.blit(line[0], line[1])

            self.surf.blit(self.enemy_pokemon_sprite, self.enemy_pokemon_sprite_rect)
            print('Drawing?')
            self.surf.blit(self.playerbox, self.playerbox_rect)
            self.surf.blit(self.enemybox, self.enemybox_rect)
            self.surf.blit(self.playerbar, self.playerbar_rect)
            self.surf.blit(self.enemybar, self.enemybar_rect)
            self.surf.blit(self.slash, self.slash_rect)
            print('Drawing?')
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

            self.surf.blit(self.player_pokemon_sprite, self.player_pokemon_sprite_rect)

            self.surf.blit(self.black_bg, self.black_bg_rect)
            self.surf.blit(self.textbox, self.textbox_rect)

            self.surf.blit(self.enemy_pokemon_sprite, self.enemy_pokemon_sprite_rect)
            #for line in self.infobox_lines:
            #    self.surf.blit(line[0], line[1])
            self.surf.blit(self.playerbox, self.playerbox_rect)
            self.surf.blit(self.enemybox, self.enemybox_rect)
            self.surf.blit(self.playerbar, self.playerbar_rect)
            self.surf.blit(self.enemybar, self.enemybar_rect)
            self.surf.blit(self.slash, self.slash_rect)
            self.surf.blit(self.top_frac, self.top_frac_rect)
            self.surf.blit(self.bot_frac, self.bot_frac_rect)
            self.surf.blit(self.level, self.level_rect)
            self.surf.blit(self.enemy_level, self.enemy_level_rect)
            self.surf.blit(self.name, self.name_rect)
            self.surf.blit(self.enemy_name, self.enemy_name_rect)
            self.surf.blit(self.battlebox, self.battlebox_rect)
            if self.selector:
                self.surf.blit(self.selector[0], self.selector[1])
            #self.surf.blit(self.battlebox_bigselect, self.battlebox_bigselect_rect)
            #pygame.image.save(self.surf, 'screen.png')
        elif self.STATE == 3:
            self.surf.fill(pygame.Color('black'))
            self.surf.blit(self.bg, self.bg_rect)
            self.surf.blit(self.fg, self.fg_rect)
            self.surf.blit(self.textbox, self.textbox_rect)
            self.surf.blit(self.playerbox, self.playerbox_rect)
            self.surf.blit(self.enemybox, self.enemybox_rect)
            
            self.surf.blit(self.battleinterface, self.battleinterface_rect)
            self.surf.blit(self.battleinterface_SURF0, self.battleinterface_TYPE0_rect)
            self.surf.blit(self.battleinterface_SURF1, self.battleinterface_TYPE1_rect)
            self.surf.blit(self.battleinterface_SURF2, self.battleinterface_TYPE2_rect)
            self.surf.blit(self.battleinterface_SURF3, self.battleinterface_TYPE3_rect)
            if self.battleinterface_MOVENAME0:
                self.surf.blit(self.battleinterface_MOVENAME0[0], self.battleinterface_MOVENAME0[1])
            if self.battleinterface_MOVENAME1:
                self.surf.blit(self.battleinterface_MOVENAME1[0], self.battleinterface_MOVENAME1[1])
            if self.battleinterface_MOVENAME2:
                self.surf.blit(self.battleinterface_MOVENAME2[0], self.battleinterface_MOVENAME2[1])
            if self.battleinterface_MOVENAME3:
                self.surf.blit(self.battleinterface_MOVENAME3[0], self.battleinterface_MOVENAME3[1])
            #self.surf.blit(self.battleinterface_GHOST, self.battleinterface_GHOST_rect)
            if self.selector:
                self.surf.blit(self.selector[0], self.selector[1])
            #pygame.image.save(self.surf, 'screen.png')

    def draw(self, screen):
        #self.surf.blit(self.battlebox, self.battlebox_rect)
        screen.blit(self.surf, self.surf.get_rect())
        #screen.blit(self.image, self.image.get_rect())

class InfoBox:
    def __init__(self):
        
        self.sentences = []
        self.sentence = None

        self.lines = []

    def add_sentences(self, sentences):
        self.sentences.insert(-1, sentences)
         
        print(self.sentence, self.sentences)

    def increment_sentences(self):
        if self.sentences:
            self.sentence = self.sentences.pop()
            self.lines = self.get_lines()
        else:
            self.sentence = None
        
    def get_lines(self):
        #if self.sentence != None:
        return textwrap.wrap(text=self.sentence, width=45)

    
    

                
        

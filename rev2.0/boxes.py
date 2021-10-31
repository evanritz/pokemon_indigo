

import textwrap
import pygame
import os

from pygame.locals import *
from consts import *
from dirs import *
from random import randrange

class Text:

    def __init__(self, text, **kwargs):

        SMALL_BM_FONT = pygame.font.Font(os.path.join(FONTS_DIR, 'AtariClassicChunky-PxXP.ttf'), 16)
        BIG_BM_FONT = pygame.font.Font(os.path.join(FONTS_DIR, 'AtariClassicChunky-PxXP.ttf'), 24)
        SM_FONT = pygame.font.Font(os.path.join(FONTS_DIR, 'AtariClassicChunky-PxXP.ttf'), 40)

        # set text
        self.text = text

        # set kwargs to inst vars
        # font_size = small or big
        # default = small
        if 'fonttype' in kwargs:
            self.font_type = kwargs['fonttype']
        else:
            self.font_type = 'small'

        # default = black
        if 'font_color' in kwargs:
            self.font_color = kwargs['font_color']
        else:
            self.font_color = Color('black')

        # links to a prev text box
        # link = left or center or right
        # linker = prev text box
        # default = center
        if 'linktype' and 'linker' in kwargs:
            self.link = kwargs['linktype']
            self.linker = kwargs['linker']
        else:
            self.link = None

        # topleft pos of text box
        # default = (0, 0)
        # if not given, link var is used
        if 'pos' and 'postype' in kwargs:
            self.pos = kwargs['pos']
            self.postype = kwargs['postype']
        else:
            self.pos = None

        # set font type
        if self.font_type == 'small':
            self.font = SMALL_BM_FONT
        elif self.font_type == 'big':
            self.font = BIG_BM_FONT
        elif self.font_type == 'start_menu':
            self.font = SM_FONT
        else:
            self.font = SMALL_BM_FONT

        self.render()

    def render(self):

        # render text into image
        self.rendered_text = self.font.render(self.text, True, self.font_color)
        # grab image rect
        self.rendered_text_rect = self.rendered_text.get_rect()

        # set rect link 
        if self.link != None:
            prev_box = self.linker.get_rendered_rect()
            if self.link == 'center':
                self.rendered_text_rect.midtop = prev_box.midbottom
            elif self.link == 'left':
                self.rendered_text_rect.topleft = prev_box.bottomleft
            elif self.link == 'right':
                self.rendered_text_rect.topright = prev_box.bottomright
        elif self.pos != None:
            if self.postype == 'center':
                self.rendered_text_rect.center = self.pos
            elif self.postype == 'left':
                self.rendered_text_rect.topleft = self.pos
            elif self.postype == 'right':
                self.rendered_text_rect.topright = self.pos

    def get_text_size(self):
        # returns the size of the text rendered in the given font
        return self.font.size(self.text)

    def get_rendered_rect(self):
        # returns the rect of the rendered text
        return self.rendered_text_rect

    def get_topleft_pos(self):
        return self.rendered_text_rect.topleft
    
    def draw(self, screen):
        screen.blit(self.rendered_text, self.rendered_text_rect)
    
class Blinker:

    # TODO: Add image for blinker
    # confimed working, just remove draw rect
    def __init__(self, images, pos, delay):
        
        self.images = images
        self.pos = pos
        self.delay = delay

        self.curr_image = self.images[0]
        self.curr_rect = self.curr_image.get_rect()
        self.curr_rect.topleft = self.pos
        self.image_idx = 0

        self.prev_ms = pygame.time.get_ticks()
        #self.is_drawing = True

    def update_pos(self, pos):
        self.pos = pos

    def update(self):
        self.curr_ms = pygame.time.get_ticks()
        if self.curr_ms-self.prev_ms >= self.delay:
            self.prev_ms = self.curr_ms
            #self.is_drawing = not self.is_drawing
            
            if self.image_idx+1 < len(self.images):
                self.image_idx += 1
            else:
                self.image_idx = 0

            self.curr_image = self.images[self.image_idx]
            self.curr_rect = self.curr_image.get_rect()
            self.curr_rect.topleft = self.pos

    def draw(self, screen):
        #if self.is_drawing:
        screen.blit(self.curr_image, self.curr_rect)

class MoveAnimator:

    def __init__(self, startpos, endpos, images, delay, move_delay):
        self.startpos = startpos
        self.endpos = endpos
        self.images = images
        self.delay = delay
        self.move_delay = move_delay

        self.dy = self.endpos[1] - self.startpos[1]
        self.dx = self.endpos[0] - self.startpos[0]

        self.pos = self.startpos

        self.blinker = Blinker(self.images, self.pos, delay)

        self.prev_ms = pygame.time.get_ticks()

    def update(self):
        #self.dx = self.startpos[0] - self.endpos[0]
        #self.dy = self.endpos[1] - self.startpos[1]
   
        self.blinker.update()

        print(self.pos)

        self.curr_ms = pygame.time.get_ticks()
        if self.curr_ms-self.prev_ms >= self.move_delay:
            self.prev_ms = self.curr_ms

            if self.pos < self.endpos:
                self.pos = (self.pos[0] + self.dx/10, self.pos[1] + self.dy/10)
                self.blinker.update_pos(self.pos)

    def draw(self, screen):
        if self.pos < self.endpos:
            self.blinker.draw(screen)



    

# text is move
# pos = topleft or topright or bottomleft or bottomright
# color is a string
class InfoBoxItem:
    def __init__(self, move, pos, color):
        self.move = move
        self.pos = pos

        self.default_color = color
        self.highlight_color = Color(*self.default_color[0:3], 0)
        self.current_color = self.default_color
        self.border = False

        if self.pos == 'topleft':
            self.rect = pygame.Rect(INFOBOX_ITEM_TOPLEFT[0], INFOBOX_ITEM_TOPLEFT[1], INFOBOX_ITEM_W, INFOBOX_ITEM_H)
        elif self.pos == 'topright':
            self.rect = pygame.Rect(INFOBOX_ITEM_TOPRIGHT[0], INFOBOX_ITEM_TOPRIGHT[1], INFOBOX_ITEM_W, INFOBOX_ITEM_H)
        elif self.pos == 'bottomleft':
            self.rect = pygame.Rect(INFOBOX_ITEM_BOTTOMLEFT[0], INFOBOX_ITEM_BOTTOMLEFT[1], INFOBOX_ITEM_W, INFOBOX_ITEM_H)
        elif self.pos == 'bottomright':
            self.rect = pygame.Rect(INFOBOX_ITEM_BOTTOMRIGHT[0], INFOBOX_ITEM_BOTTOMRIGHT[1], INFOBOX_ITEM_W, INFOBOX_ITEM_H)

        self.render()

    def render(self):
        self.text_box = Text(self.move.capitalize(), pos=self.rect.center, postype='center', fonttype='big')
    
    def highlight(self):
        self.border = True
    
    def unhighlight(self):
        self.border = False

    def  get_move(self):
        return self.move

    def draw(self, screen):

        if self.border:
            pygame.draw.rect(screen, Color('black'), self.rect.inflate(5, 5), border_radius=5)

        pygame.draw.rect(screen, Color(self.current_color), self.rect, border_radius=5)
        self.text_box.draw(screen)
    

class InfoBox:

    current_pokemon = None

    def __init__(self, mode, sentences):

        # set mode and sentences
        self.mode = mode
        self.sentences = sentences
        self.sentences.reverse()

        # set last sentence 
        self.sentence = self.sentences[-1]
        
        # stores the text boxes
        self.text_boxes = []

        # stores the move boxes
        self.move_boxes = []

        # stores moves text
        self.moves = []

        self.selected_move = None
        self.selected_option = None 

        self.move_animation = None

        # user idx on the button they are on
        self.user_idx = [0, 0]

        self.flag = None

        
        # create pos
        self.pos = INFOBOX_ITEMS_TOPLEFT

        # load infobox texture and scale to rez
        self.image = pygame.image.load(os.path.join(MENU_TEXTURES_DIR, 'canvas.png'))
        self.image = pygame.transform.scale(self.image, (INFOBOX_W, INFOBOX_H))

        # get rectangle of scaled image and set topleft pos
        self.rect = self.image.get_rect()
        self.rect.topleft = INFOBOX_TOPLEFT

        self.rect = pygame.Rect(INFOBOX_TOPLEFT[0], INFOBOX_TOPLEFT[1], INFOBOX_W, INFOBOX_H)

        self.blinker_images = [
            pygame.transform.scale(pygame.image.load(os.path.join(MENU_TEXTURES_DIR, 'book_closed.png')), (36, 48)),
            pygame.transform.scale(pygame.image.load(os.path.join(MENU_TEXTURES_DIR, 'book_open_1.png')), (36, 48)),
            #pygame.transform.scale(pygame.image.load(os.path.join(MENU_TEXTURES_DIR, 'book_open_2.png')), (36, 48)),
            pygame.transform.scale(pygame.image.load(os.path.join(MENU_TEXTURES_DIR, 'book_open_3.png')), (48, 48)),
            pygame.transform.scale(pygame.image.load(os.path.join(MENU_TEXTURES_DIR, 'book_opened.png')), (48, 48))
        ]

        self.blinker = Blinker(self.blinker_images, (self.rect.midright[0]-100, self.rect.midright[1]-32), 1000)

        self.move_images = [
            pygame.transform.scale(pygame.image.load(os.path.join(POKEMON_SPRITES_DIR, 'fire1.png')), (96, 96)),
            pygame.transform.scale(pygame.image.load(os.path.join(POKEMON_SPRITES_DIR, 'fire2.png')), (96, 96)),
            pygame.transform.scale(pygame.image.load(os.path.join(POKEMON_SPRITES_DIR, 'lightning1.png')), (96, 96)),
            pygame.transform.scale(pygame.image.load(os.path.join(POKEMON_SPRITES_DIR, 'lightning2.png')), (96, 96)),
            pygame.transform.scale(pygame.image.load(os.path.join(POKEMON_SPRITES_DIR, 'leaf1.png')), (96, 96)),
            pygame.transform.scale(pygame.image.load(os.path.join(POKEMON_SPRITES_DIR, 'leaf2.png')), (96, 96)),
            pygame.transform.scale(pygame.image.load(os.path.join(POKEMON_SPRITES_DIR, 'leaf3.png')), (96, 96)),
            pygame.transform.scale(pygame.image.load(os.path.join(POKEMON_SPRITES_DIR, 'bubbles1.png')), (96, 96)),
            pygame.transform.scale(pygame.image.load(os.path.join(POKEMON_SPRITES_DIR, 'bubbles2.png')), (96, 96))
        ]

        self.move_images[2] = pygame.transform.rotate(self.move_images[2], -225)
        self.move_images[3] = pygame.transform.rotate(self.move_images[3], -225)

        self.word_wrap(self.sentence)
        self.text_render()

       

    def word_wrap(self, sentence):
        self.lines = textwrap.wrap(text=sentence, width=50) # fontsize of char / width of infobox - like 5

    def text_render(self):

        text_box = Text(self.lines[0], pos=self.pos, postype='left')
        self.text_boxes.append(text_box)

        # i for line idx 
        # j for text box idx
        for i in range(1, len(self.lines)):
            j = i - 1
            text_box = Text(self.lines[i], linktype='left', linker=self.text_boxes[j])
            self.text_boxes.append(text_box)
    
    def moves_render(self):
        self.move_boxes = [
            [InfoBoxItem(self.moves[0], 'topleft', Color('blue')), InfoBoxItem(self.moves[1], 'topright', Color('yellow'))],
            [InfoBoxItem(self.moves[2], 'bottomleft', Color('green')), InfoBoxItem(self.moves[3], 'bottomright', Color('red'))],
        ]
        self.move_boxes[self.user_idx[0]][self.user_idx[1]].highlight()

    def move_moves(self, dir):  
        
        self.move_boxes[self.user_idx[0]][self.user_idx[1]].unhighlight()

        if dir == 'up':
            self.user_idx[0] = 0
        elif dir == 'down':
            self.user_idx[0] = 1
        elif dir == 'left':
            self.user_idx[1] = 0
        elif dir == 'right':
            self.user_idx[1] = 1
        
        self.move_boxes[self.user_idx[0]][self.user_idx[1]].highlight()

    def select_move(self):
        self.selected_move = self.move_boxes[self.user_idx[0]][self.user_idx[1]].get_move()
        if InfoBox.current_pokemon == 'Squirtle':
            self.add_moves(['Splash', 'BubbleBeam', 'Flood', 'Wet'])
            self.move_animation = MoveAnimator(PlayerBox.sprite_rect.center, EnemyBox.sprite_rect.center, self.move_images[7:9], 100, 200)
        elif InfoBox.current_pokemon == 'Pikachu':
            self.add_moves(['Zap', 'Discharge', 'Spark', 'TailWhip'])
            self.move_animation = MoveAnimator(PlayerBox.sprite_rect.center, EnemyBox.sprite_rect.center, self.move_images[2:4], 100, 200)
        elif InfoBox.current_pokemon == 'Bulbasaur':
            self.add_moves(['Seed Bomb', 'RazorLeaf', 'VineWhip', 'Tackle'])
            self.move_animation = MoveAnimator(PlayerBox.sprite_rect.center, EnemyBox.sprite_rect.center, self.move_images[4:6], 100, 200)
        elif InfoBox.current_pokemon == 'Charmander':
            self.add_moves(['FireFang', 'Ember', 'FireSpin', 'SmokeScreen'])
            self.move_animation = MoveAnimator(PlayerBox.sprite_rect.center, EnemyBox.sprite_rect.center, self.move_images[0:2], 100, 200)

    def select_option(self):
        self.selected_option = self.move_boxes[self.user_idx[0]][self.user_idx[1]].get_move()
        InfoBox.current_pokemon = self.selected_option
        self.add_sentences(['You have choosen {}. Take care of your Pokemon.'.format(self.selected_option), 'You ready to explore the WORLD OF POKEMON!', 'TRANS'])
        self.set_mode('text')

       
        player_sprites_files = os.listdir(POKEMON_SPRITES_DIR)
        #print(player_sprites_files)
        player_sprite_file = None
        for sprite_file in player_sprites_files:
            #print(sprite_file, self.selected_option)
            if self.selected_option.lower() in sprite_file: 
                player_sprite_file = sprite_file

        name = player_sprite_file.split('_')[0]

        PlayerBox.details_box = DetailsBox(PlayerBox.details_rect, 'left',PLAYERBOX_INFO_CENTER, {'max_health': 100, 'health': 100, 'xp': 0, 'max_xp': 300, 'level': 5, 'name': name})
        PlayerBox.sprite_box = Image(player_sprite_file, PlayerBox.sprite_rect, (384, 384), postype='center', pos=PlayerBox.sprite_rect.center)

    def set_moves(self):
        if InfoBox.current_pokemon != None:
                if InfoBox.current_pokemon == 'Squirtle':
                    self.add_moves(['Splash', 'BubbleBeam', 'Flood', 'Wet'])
                elif InfoBox.current_pokemon == 'Pikachu':
                    self.add_moves(['Zap', 'Discharge', 'Spark', 'TailWhip'])
                elif InfoBox.current_pokemon == 'Bulbasaur':
                    self.add_moves(['Seed Bomb', 'RazorLeaf', 'VineWhip', 'Tackle'])
                elif InfoBox.current_pokemon == 'Charmander':
                    self.add_moves(['FireFang', 'Ember', 'FireSpin', 'SmokeScreen'])

    def add_sentences(self, sentences):
        for sentence in sentences:
            self.sentences.insert(0, sentence)
        self.sentence = self.sentences[-1]
        self.word_wrap(self.sentence)

    def increment_sentence(self):
        self.text_boxes = []

        if len(self.sentences) > 0:
            self.sentence = self.sentences.pop()
            if self.sentence == 'TRANS':
                self.flag = 'game'
            else:
                self.word_wrap(self.sentence)
                self.text_render()
        elif len(self.sentences) == 0:
            self.lines = []
            self.set_mode('battle')

    def add_moves(self, moves):
        self.moves = []
        self.moves = moves
        self.moves_render()

    def set_mode(self, mode):
        self.mode = mode
        if self.mode == 'text':
            self.text_render()
        elif self.mode == 'battle':
            
            print(self.moves)

            self.moves_render()

    def check_flag(self):
        flag = self.flag
        self.flag = None
        return flag

    def draw(self, screen):

        
        self.blinker.update()

        
        #screen.blit(self.image, self.rect)

        pygame.draw.rect(screen, Color('black'), self.rect)
        pygame.draw.rect(screen, Color('gray'), self.rect.inflate(-10, -10), border_radius=5)
        pygame.draw.rect(screen, Color('black'), self.rect.inflate(-15, -15), border_radius=5)
        pygame.draw.rect(screen, Color('white'), self.rect.inflate(-20, -20), border_radius=5)
        pygame.draw.rect(screen, Color('black'), self.rect.inflate(-25, -25), border_radius=5)
        #pygame.draw.rect(screen, Color(75, 0, 130), self.rect.inflate(-35, -35), border_radius=5)
        pygame.draw.rect(screen, Color('white'), self.rect.inflate(-45, -45), border_radius=5)
        

        if self.mode == 'text':
            for text_box in self.text_boxes:
                text_box.draw(screen)
            
            self.blinker.draw(screen)
            
        elif self.mode == 'battle':

            if self.move_animation != None:
                self.move_animation.update()
                self.move_animation.draw(screen)

            for move_box_row in self.move_boxes:
                for move_box in move_box_row:
                    move_box.draw(screen)

class StatusBar:

    def __init__(self, curr, max, color, **kwargs):
        
        self.curr = curr
        self.max = max
        self.color = color

         # links to a prev text box
        # link = left or center or right
        # linker = prev text box
        # default = center
        if 'linktype' and 'linker' in kwargs:
            self.link = kwargs['linktype']
            self.linker = kwargs['linker']
        else:
            self.link = None

        # topleft pos of text box
        # default = (0, 0)
        # if not given, link var is used
        if 'pos' and 'postype' in kwargs:
            self.pos = kwargs['pos']
            self.postype = kwargs['postype']
        else:
            self.pos = None

        self.ratio = self.curr/self.max

        self.render()

    def render(self):

        # background rect
        self.bg_rect = pygame.Rect(0, 0, STATUSBAR_W, STATUSBAR_H)

        # foreground rect
        self.fg_rect = pygame.Rect(0, 0, int(STATUSBAR_W*self.ratio), STATUSBAR_H)

        # set rect link 
        if self.link != None:
            prev_box = self.linker.get_rendered_rect()
            if self.link == 'center':
                self.bg_rect.midtop = prev_box.midbottom
                self.fg_rect.midtop = prev_box.midbottom
            elif self.link == 'left':
                self.bg_rect.topleft = prev_box.bottomleft
                self.fg_rect.topleft = prev_box.bottomleft
            elif self.link == 'right':
                self.bg_rect.topright = prev_box.bottomright
                self.fg_rect.topright = prev_box.bottomright
        elif self.pos != None:
            if self.postype == 'center':
                self.bg_rect.center = self.pos
                self.fg_rect.center = self.pos
            elif self.postype == 'left':
                self.bg_rect.topleft = self.pos
                self.fg_rect.topleft = self.pos
            elif self.postype == 'right':
                self.bg_rect.topright = self.pos
                self.fg_rect.topright = self.pos

    def get_rendered_rect(self):
        return self.bg_rect

    def draw(self, screen):

        pygame.draw.rect(screen, Color('lightgray'), self.bg_rect, border_radius=10)
        pygame.draw.rect(screen, self.color, self.fg_rect, border_radius=10)


class Image:

    def __init__(self, file_name, rect, rez, **kwargs):
        self.file_name = file_name
        self.rect = rect
        self.rez = rez

        if 'frames' in kwargs:
            self.frames = kwargs['frames']

        if 'pos' and 'postype' in kwargs:
            self.pos = kwargs['pos']
            self.postype = kwargs['postype']

        self.image = pygame.image.load(os.path.join(POKEMON_SPRITES_DIR, self.file_name))
        self.image = pygame.transform.scale(self.image, self.rez)
        self.image_rect = self.image.get_rect()

        self.render()

    def render(self):

        if self.pos != None:
            if self.postype == 'center':
                self.image_rect.center = self.pos
            elif self.postype == 'left':
                self.image_rect.topleft = self.pos
            elif self.postype == 'right':
                self.image_rect.topright = self.pos
            
            elif self.postype == 'bottom':
                self.image_rect.midbottom = self.pos
    
    def draw(self, screen):
        screen.blit(self.image, self.image_rect)


# pokemon dict keys = max_health, health, xp, max_xp, level, name
class DetailsBox:

    def __init__(self, rect, postype, pos, pokemon_dict):
        self.pokemon_dict = pokemon_dict
        self.rect = rect
        self.postype = postype
        self.pos = pos

        self.text_boxes = []

        self.bg_rect = pygame.Rect(self.rect.midtop[0], self.rect.midtop[1], 200, 90)
        self.bg_rect.center = self.pos

        self.render()

    def update(self, key, val):
        self.pokemon_dict[key] = val
        self.text_boxes = []
        self.render()

    def get_val(self, key):
        return self.pokemon_dict[key]
        
    def render(self):
    
        name_text_box = Text(self.pokemon_dict['name'].upper(), postype=self.postype, pos=self.bg_rect.topleft)
        self.text_boxes.append(name_text_box)

        level_text_box = Text('LV: {}'.format(self.pokemon_dict['level']), linktype='left', linker=name_text_box)
        self.text_boxes.append(level_text_box)

        xp_bar_box = StatusBar(self.pokemon_dict['xp'], self.pokemon_dict['max_xp'], Color('cyan'), linktype='left', linker=level_text_box)
        self.text_boxes.append(xp_bar_box)

        health_fract_text_box = Text('HP: {} / {}'.format(self.pokemon_dict['health'], self.pokemon_dict['max_health']), linktype='left', linker=xp_bar_box)
        self.text_boxes.append(health_fract_text_box)

        health_bar_box = StatusBar(self.pokemon_dict['health'], self.pokemon_dict['max_health'], Color('green'), linktype='left', linker=health_fract_text_box)
        self.text_boxes.append(health_bar_box)

    def draw(self, screen):

        pygame.draw.rect(screen, Color('black'), self.bg_rect.inflate(10, 10), border_radius=5)
        pygame.draw.rect(screen, Color('white'), self.bg_rect, border_radius=5)

        #pygame.draw.circle(screen, Color('black'), PLAYERBOX_INFO_CENTER, 10)
        
        for text_box in self.text_boxes:
            text_box.draw(screen)

class EnemyBox:

    sprite_rect = pygame.Rect(ENEMYBOX_SPRITE_TOPLEFT[0], ENEMYBOX_SPRITE_TOPLEFT[1], ENEMYBOX_SPRITE_W, ENEMYBOX_SPRITE_H)

    def __init__(self):
        
        self.rect = pygame.Rect(ENEMYBOX_TOPLEFT[0], ENEMYBOX_TOPLEFT[1], ENEMYBOX_W, ENEMYBOX_H)
        self.details_rect = pygame.Rect(ENEMYBOX_INFO_TOPLEFT[0], ENEMYBOX_INFO_TOPLEFT[1], ENEMYBOX_INFO_W, ENEMYBOX_INFO_H)
        

        self.details_box = DetailsBox(self.details_rect,'left', ENEMYBOX_INFO_CENTER, {'max_health': 100, 'health': 75, 'xp': 300, 'max_xp': 456, 'level': 12, 'name': 'Evanmon'})

        self.sprite_box = Image('alakazam_front_2.png', PlayerBox.sprite_rect, (192, 192), postype='bottom', pos=PlayerBox.sprite_rect.midbottom)

        self.enemy_sprites_files = [f for f in os.listdir(POKEMON_SPRITES_DIR) if 'front' in f]
        print(len(self.enemy_sprites_files))
        

    def generate(self):
        #self.details_box = DetailsBox(self.details_rect,'left', ENEMYBOX_INFO_CENTER, {'max_health': 100, 'health': 75, 'xp': 300, 'max_xp': 456, 'level': 12, 'name': 'Evanmon'})
        sprite_file = self.enemy_sprites_files[randrange(0, len(self.enemy_sprites_files)-1)]
        self.sprite_box = Image(sprite_file, self.sprite_rect, (192, 192), postype='bottom', pos=self.sprite_rect.midbottom)

        # pokemon dict keys = max_health, health, xp, max_xp, level, name
        print(sprite_file)
        name, _ = sprite_file.split('_')
        self.details_box.update('name', name)
        health = randrange(25, 100)
        self.details_box.update('max_health', health)
        self.details_box.update('health', health)
        self.details_box.update('xp', randrange(0, 255))
        self.details_box.update('max_xp', 255)
        self.details_box.update('level', randrange(1, 25))

    def get_center(self):
        return self.sprite_rect.center

    def render(self):
        print()

    def draw(self, screen):

        #pygame.draw.circle(screen, Color('purple'), self.details_rect.center, 10)
        self.sprite_box.draw(screen)
        self.details_box.draw(screen)

class PlayerBox:

    details_box = None
    sprite_box = None

    details_rect = pygame.Rect(PLAYERBOX_INFO_TOPLEFT[0], PLAYERBOX_INFO_TOPLEFT[1], PLAYERBOX_INFO_W, PLAYERBOX_INFO_H)
    sprite_rect = pygame.Rect(PLAYERBOX_SPRITE_TOPLEFT[0], PLAYERBOX_SPRITE_TOPLEFT[1], PLAYERBOX_SPRITE_W, PLAYERBOX_SPRITE_H)

    def __init__(self):
        
        self.rect = pygame.Rect(PLAYERBOX_TOPLEFT[0], PLAYERBOX_TOPLEFT[1], PLAYERBOX_W, PLAYERBOX_H)


    def draw(self, screen):

        #pygame.draw.circle(screen, Color('purple'), PlayerBox.details_rect.center, 10)
        PlayerBox.sprite_box.draw(screen)
        PlayerBox.details_box.draw(screen)
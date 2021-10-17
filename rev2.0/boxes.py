

import textwrap
import pygame
import os

from pygame.locals import *
from consts import *
from dirs import *

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
        self.image_idx = 0

        self.prev_ms = pygame.time.get_ticks()
        #self.is_drawing = True

    
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
            self.curr_rect.topleft = self.pos

    def draw(self, screen):
        #if self.is_drawing:
        screen.blit(self.curr_image, self.curr_rect)
            

# text is move
# pos = topleft or topright or bottomleft or bottomright
# color is a string
class InfoBoxItem:
    def __init__(self, move, pos, color):
        self.move = move
        self.pos = pos

        self.default_color = color
        self.highlight_color = Color(*self.default_color[0:3], 0)
        print(self.highlight_color)
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

    def get_move(self):
        return self.move

    def draw(self, screen):

        if self.border:
            pygame.draw.rect(screen, Color('black'), self.rect.inflate(5, 5), border_radius=5)

        pygame.draw.rect(screen, Color(self.current_color), self.rect, border_radius=5)
        self.text_box.draw(screen)
    

class InfoBox:

    def __init__(self, mode, sentences):

        # set mode and sentences
        self.mode = mode
        self.sentences = sentences

        # set last sentence 
        self.sentence = self.sentences[-1]

        # stores the text boxes
        self.text_boxes = []

        # stores the move boxes
        self.move_boxes = []

        # stores moves text
        self.moves = []

        # user idx on the button they are on
        self.user_idx = [0, 0]

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
        return self.move_boxes[self.user_idx[0]][self.user_idx[1]].get_move()

    def add_sentences(self, sentences):
        for sentence in sentences:
            self.sentences.insert(0, sentence)

    def increment_sentence(self):
        self.text_boxes = []
        self.word_wrap(self.sentence)
        self.text_render()

        if len(self.sentences) > 0:
            self.sentence = self.sentences.pop()

    def add_moves(self, moves):
        self.moves = moves

    def set_mode(self, mode):
        self.mode = mode
        if self.mode == 'text':
            self.text_render()
        elif self.mode == 'battle':
            print(self.moves)
            self.moves_render()
            
    def draw(self, screen):

        self.blinker.update()

        #screen.blit(self.image, self.rect)

        pygame.draw.rect(screen, Color('black'), self.rect)
        pygame.draw.rect(screen, Color('gray'), self.rect.inflate(-10, -10), border_radius=5)
        pygame.draw.rect(screen, Color('black'), self.rect.inflate(-15, -15), border_radius=5)
        pygame.draw.rect(screen, Color('white'), self.rect.inflate(-20, -20), border_radius=5)
        pygame.draw.rect(screen, Color('black'), self.rect.inflate(-25, -25), border_radius=5)
        pygame.draw.rect(screen, Color(75, 0, 130), self.rect.inflate(-35, -35), border_radius=5)
        pygame.draw.rect(screen, Color('white'), self.rect.inflate(-45, -45), border_radius=5)
        

        if self.mode == 'text':
            for text_box in self.text_boxes:
                text_box.draw(screen)
            
            self.blinker.draw(screen)
            
        elif self.mode == 'battle':
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

        #print(self.bg_rect, self.fg_rect)
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
        self.render()
        
    def render(self):
    
        name_text_box = Text(self.pokemon_dict['name'], fonttype='big', postype=self.postype, pos=self.bg_rect.topleft)
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

class SpriteBox:

    def __init__(self, rect):
        self.rect = rect


class EnemyBox:

    def __init__(self):
        
        self.rect = pygame.Rect(ENEMYBOX_TOPLEFT[0], ENEMYBOX_TOPLEFT[1], ENEMYBOX_W, ENEMYBOX_H)
        self.details_rect = pygame.Rect(ENEMYBOX_INFO_TOPLEFT[0], ENEMYBOX_INFO_TOPLEFT[1], ENEMYBOX_INFO_W, ENEMYBOX_INFO_H)
        self.sprite_rect = pygame.Rect(ENEMYBOX_SPRITE_TOPLEFT[0], ENEMYBOX_SPRITE_TOPLEFT[1], ENEMYBOX_SPRITE_W, ENEMYBOX_SPRITE_H)

        self.details_box = DetailsBox(self.details_rect,'left', ENEMYBOX_INFO_CENTER, {'max_health': 100, 'health': 75, 'xp': 300, 'max_xp': 456, 'level': 12, 'name': 'Evanmon'})

        self.sprite_box = Image('alakazam_front_2.png', self.sprite_rect, (192, 192), postype='bottom', pos=self.sprite_rect.midbottom)

    def render(self):
        print()

    def draw(self, screen):

        #pygame.draw.circle(screen, Color('purple'), self.details_rect.center, 10)
        self.sprite_box.draw(screen)
        self.details_box.draw(screen)

class PlayerBox:

    def __init__(self):
        
        self.rect = pygame.Rect(PLAYERBOX_TOPLEFT[0], PLAYERBOX_TOPLEFT[1], PLAYERBOX_W, PLAYERBOX_H)
        self.details_rect = pygame.Rect(PLAYERBOX_INFO_TOPLEFT[0], PLAYERBOX_INFO_TOPLEFT[1], PLAYERBOX_INFO_W, PLAYERBOX_INFO_H)
        self.sprite_rect = pygame.Rect(PLAYERBOX_SPRITE_TOPLEFT[0], PLAYERBOX_SPRITE_TOPLEFT[1], PLAYERBOX_SPRITE_W, PLAYERBOX_SPRITE_H)

        self.details_box = DetailsBox(self.details_rect, 'left',PLAYERBOX_INFO_CENTER, {'max_health': 100, 'health': 75, 'xp': 300, 'max_xp': 456, 'level': 12, 'name': 'Nhatmon'})

        self.sprite_box = Image('alakazam_back_2.png', self.sprite_rect, (384, 384), postype='center', pos=self.sprite_rect.center)

    def draw(self, screen):

        pygame.draw.circle(screen, Color('purple'), self.details_rect.center, 10)
        #print(self.details_rect.center)
        self.sprite_box.draw(screen)
        self.details_box.draw(screen)
'''
nodes.py

Holds all different types of Nodes

rev1.0 - 9/17/21
Created base Node Class


Written by Evan
'''

# all of these can be overwriting using kwargs on the init of a new node object
# gap = (x, y) gap between each node on a scene
# size = (w, h) size of the node
# dir = (bool, bool) = (x dir, y dir) direction of the sequential nodes
# pos = (x, y) start coords of the a node, always the TOPLEFT

import os
import pygame
import textwrap
from pygame.locals import *
from coords import ScreenCoords
from screen_grid import BattleSelectionBox, ColoredStatusBar, EnemyPokemonBox, MainBox, PlayerPokemonBox, BattleSelectionItemBox, ScreenGrid

class Node:

    id = 0

    # default settings
    pos = (0, 0)
    size = (0, 0)
    dir = (False, False)
    gap = (0, 0)

    def __init__(self, **kwargs):

        self.id = Node.id
        Node.id += 1

        if 'pos' in kwargs:
            Node.pos = kwargs['pos']

        if 'size' in kwargs:
            Node.size = kwargs['size']

        if 'dir' in kwargs:
            Node.dir = kwargs['dir']

        if 'gap' in kwargs:
            Node.gap = kwargs['gap']

    def child_update(self):
        # Text and other classes are children classes of Node, they have different sizes 
        # based on the content they hold.
        # The child will update there parent with there needed size

        self.pos = Node.pos

        if Node.dir[0]: # x dir
            Node.pos = (Node.pos[0] + Node.size[0] + Node.gap[0], Node.pos[1])
        if Node.dir[1]: # y dir
            Node.pos = (Node.pos[0], Node.pos[1] + Node.size[1] + Node.gap[1])

    # Resets static vars
    def reset():

        Node.pos = (0, 0)
        Node.size = (0, 0)
        Node.dir = (False, False)
        Node.gap = (0, 0)


# Nodes can be added to a group
# All Nodes must be given at init of group object
# Can pass either a single Node or a list of Nodes
# Group needs a name. You can access it in the scene dict using its name
class Group:
    def __init__(self, name, nodes):

        if isinstance(nodes, list):
            self.nodes = nodes
        else:
            self.nodes = [nodes]

        self.name = name
        Node.reset()

    def get_nodes(self):
        return self.nodes

    def get_name(self):
        return self.name

    def draw(self, screen):
        for node in self.nodes:
            node.draw(screen)

# text node displays text to scene
# text node is sized based on its contents and fontsize
class Text(Node):
    
    font_color = Color('white')

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)

        self.text = text
        
        self.font_name = os.path.join('fonts', 'AtariClassicChunky-PxXP.ttf')
        self.font_size = 24

        if 'font_color' in kwargs:
            Text.font_color = kwargs['font_color']

        if 'font_size' in kwargs:
            self.font_size = kwargs['font_size']

        if 'font_name' in kwargs:
            self.font_name = kwargs['font_name']


        self.set_font()
        self.render()

        self.child_update()

    def set_font(self):
        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.node_size = self.font.size(self.text)
        Node.size = self.node_size
    
    def render(self):
        self.image = self.font.render(self.text, True, Text.font_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = Node.pos

    def get_rect(self):
        return self.rect

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# text main is the main text box in the game, positioned in the bottom center of the screen
# pass a list of sentences e.g ['hello m8', 'whats up today', etc]
class TextMain(Node):

    def __init__(self, sentences, **kwargs):
        super().__init__(**kwargs)

        self.sentences = sentences
        self.sentence = self.sentences[len(self.sentences)-1]

        self.text_nodes = []

        self.font_name = os.path.join('fonts', 'AtariClassicChunky-PxXP.ttf')
        self.font_size = 24
        self.font_color = Color('black')

        self.delay_time = 0

        self.rect = MainBox()

        self.loading_blink_pts = []
        #self.loading_blink_pts.append((self.rect.w14, self.rect.h7))
        #self.loading_blink_pts.append((self.rect.w15, self.rect.h9))
        #self.loading_blink_pts.append((self.rect.w, self.rect.h9))


        self.set_font()
        self.word_wrap(self.sentence)
        self.render()

    # keybind function for incrementing to next sentence
    def increment_text(self):

        self.text_nodes = []
        self.word_wrap(self.sentence)
        self.render()

        if len(self.sentences) > 0:
            self.sentence = self.sentences.pop()    
        
    # add a sentence or sentences as a list
    def add_sentences(self, sentences):
        for sentence in sentences:
            self.sentences.insert(0, sentence)

    def set_font(self):
        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.font_size_per_char = self.font.size('a')
        self.chars_per_line = (self.rect.w-(self.rect.w-self.rect.w1))//self.font_size_per_char[0] #+ 17
        Node.size = (self.rect.w, self.rect.h)

    # pass a sentence and push it to a newline if its longer then text box width
    def word_wrap(self, sentence):
        self.lines = textwrap.wrap(text=sentence, width=self.chars_per_line)

    # render a sentence into image/s of text
    def render(self):

        text_node = Text(self.lines[0], pos=(self.rect.w1, self.rect.h1), gap=(0, 10), dir=(False, True), font_color=Color('black'), font_size=self.font_size, font_name=self.font_name)
        self.text_nodes.append(text_node)

        for line in self.lines[1:len(self.lines)]:
            text_node = Text(line)
            self.text_nodes.append(text_node)
    
    def draw(self, screen):

        pygame.draw.line(screen, Color('red'), (0, ScreenCoords.four_eighths_h), (ScreenCoords.w, ScreenCoords.four_eighths_h))
        pygame.draw.line(screen, Color('red'), (ScreenCoords.four_eighths_w, 0), (ScreenCoords.four_eighths_w, ScreenCoords.h))

        pygame.draw.rect(screen, Color('black'), self.rect.inflate(10, 10), border_radius=3)
        pygame.draw.rect(screen, Color('white'), self.rect, border_radius=1)
        pygame.draw.rect(screen, Color('blue'), BattleSelectionBox())

        x =  BattleSelectionItemBox('topleft')
        pygame.draw.rect(screen, Color('purple'), x)

        x =  BattleSelectionItemBox('topright')
        pygame.draw.rect(screen, Color('purple'), x)

        x =  BattleSelectionItemBox('bottomleft')
        pygame.draw.rect(screen, Color('purple'), x)

        x =  BattleSelectionItemBox('bottomright')
        pygame.draw.rect(screen, Color('purple'), x)

        for text_node in self.text_nodes:
            text_node.draw(screen)

        self.delay_time += 1
        if self.delay_time <= 50:
            x = 1
            #pygame.draw.polygon(screen, Color('black'), self.loading_blink_pts)
        elif self.delay_time == 100:
            self.delay_time = 0
            

class TextStartMenu(Node):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.font_name = os.path.join('fonts', 'PokemonSolidNormal-xyWR.ttf')
        self.font_size = 96
        self.font_color = Color('blue')
        self.delay = 0

        self.nodes = []

        self.menu_title_text = 'POKEMON INDIGO'
        self.menu_flashing_text = 'Press SPACE to Start'

        self.set_font()
        self.render()

    def set_font(self):
        self.font = pygame.font.Font(self.font_name, self.font_size)
        Node.size = (ScreenGrid.w, ScreenGrid.h)

    def render(self):
        self.menu_title_text_node = Text(self.menu_title_text, font_name=self.font_name, font_size=self.font_size, font_color=self.font_color)    
        self.menu_title_text_node.get_rect().center = (ScreenGrid.center[0], ScreenGrid.h4)
        self.menu_flashing_text = Text(self.menu_flashing_text, font_color=Color('black'))
        self.menu_flashing_text.get_rect().center = (ScreenGrid.center[0], ScreenGrid.h8)

    def draw(self, screen):

        self.menu_title_text_node.draw(screen)

        self.delay += 1
        if self.delay <= 25:
            self.menu_flashing_text.draw(screen)
        elif self.delay == 50:
            self.delay = 0
            


# TextPokemon is the battle stats of pokemon during a battle
# pokemon_sprites consists of front and back sprites of pokemon e.g 0 = back 1 = front
# pokemon_traits consists of [health, xp]
# pokemon_consts consists of [name, level, max_xp, max_health]
# user can ONLY be 'enemy' or 'player'
class TextPokemon(Node):



    def __init__(self, pokemon_sprites, pokemon_traits, pokemon_consts, user, **kwargs):
        super().__init__(**kwargs)

        self.pokemon_sprites = pokemon_sprites
        self.pokemon_traits = pokemon_traits
        self.pokemon_consts = pokemon_consts

        self.user = user

        self.name = self.pokemon_consts[0]
        self.level = self.pokemon_consts[1]
        self.max_health = self.pokemon_consts[2]
        self.max_xp = self.pokemon_consts[3]

        self.image = None

        self.nodes = []

        self.font_name = os.path.join('fonts', 'AtariClassicChunky-PxXP.ttf')
        self.font_size = 48
        self.font_color = Color('black')

        if self.user == 'player':
            self.rect = PlayerPokemonBox()
            self.sprite_image = self.pokemon_sprites[0]

        elif self.user == 'enemy':
            self.rect = EnemyPokemonBox()
            self.sprite_image = self.pokemon_sprites[1]

        self.sprite_rect = self.sprite_image.get_rect()
        self.sprite_rect.center = self.rect.midbottom

        self.render()

    def render(self):
        name_text_node = Text(self.name, dir=(False, True), gap=(10, 10), pos=(self.rect.w1, self.rect.h1), font_name=self.font_name, font_size=self.font_size, font_color=self.font_color)
        self.nodes.append(name_text_node)
      
        level_text_node = Text('Lv: ' + str(self.level), dir=(False, True))
        self.nodes.append(level_text_node)

        current_health_text_node = Text(str(self.pokemon_traits[0]) + ' / ', dir=(True, False))
        self.nodes.append(current_health_text_node)
        
        max_health_text_node = Text(str(self.max_health), dir=(False, True))
        self.nodes.append(max_health_text_node)

        health_bar_text_node = Text('HP:', dir=(True, False), pos=(self.rect.w1, Node.pos[1]))
        self.nodes.append(health_bar_text_node)

        health_bar = StatusBar(self.pokemon_traits[0], self.max_health, color=Color('green'), dir=(False, True))
        self.nodes.append(health_bar)

        xp_bar_text_node = Text('XP:', dir=(True, False), pos=(self.rect.w1, Node.pos[1]))
        self.nodes.append(xp_bar_text_node)
        xp_bar = StatusBar(self.pokemon_traits[1], self.max_xp, color=Color('purple'), dir=(False, True))
        self.nodes.append(xp_bar)


    
    def update_vals(self, pokemon_traits):
        self.pokemon_traits = pokemon_traits
        self.nodes = []
        self.render()

    def draw(self, screen):

        #pygame.draw.rect(screen, Color('white'), self.rect)

        for node in self.nodes:
            node.draw(screen)

        screen.blit(self.sprite_image, self.sprite_rect)

class StatusBar(Node):

    def __init__(self, curr, max, **kwargs):
        super().__init__(**kwargs)
        self.curr = curr
        self.max = max

        self.ratio = self.curr/self.max

        self.file = None
        self.background = None

        self.rect = ColoredStatusBar()

        self.scaled_w = int(self.rect.w*self.ratio)
        #self.scaled_rect = self.rect
        self.scaled_rect = pygame.Rect(0, 0, self.scaled_w, self.rect.h)
        

        #if 'file' in kwargs:
        #   self.file = kwargs['file']

        if 'background' in kwargs:
            self.background = kwargs['background']

        if 'color' in kwargs:
            self.color = kwargs['color']

        self.set_size()
        self.render()

        self.child_update()

    def set_size(self):
        Node.size = (self.scaled_rect.w, self.scaled_rect.h)
        
    def render(self):
        self.scaled_rect.topleft = Node.pos

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.scaled_rect)


        


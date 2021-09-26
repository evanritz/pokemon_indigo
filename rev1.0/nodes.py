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

import pygame
import textwrap
from pygame.locals import *
from coords import ScreenCoords

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
# Group needs a name. You can access it in the scene dict using its name
class Group:
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes
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

        self.font_name = None
        self.font_size = 48

        if 'font_color' in kwargs:
            Text.font_color = kwargs['font_color']

        self.set_font()
        self.render()

        self.child_update()

    def set_font(self):
        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.font_size = self.font.size(self.text)
        Node.size = self.font_size
    
    def render(self):
        self.image = self.font.render(self.text, True, Text.font_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = Node.pos

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

        self.font_name = None
        self.font_size = 48
        self.font_color = Color('black')

        self.rect = pygame.Rect(ScreenCoords.two_eighths_w, ScreenCoords.six_eighths_h, ScreenCoords.four_eighths_w, ScreenCoords.two_eighths_h)

        self.set_font()
        self.word_wrap(self.sentence)
        self.render()

    # keybind function for incrementing to next sentence
    def increment_text(self):

        print('Running increment_text()')
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
        self.chars_per_line = self.rect.w//self.font_size_per_char[0] #+ 17
        Node.size = (self.rect.w, self.rect.h)

    # pass a sentence and push it to a newline if its longer then text box width
    def word_wrap(self, sentence):
        self.lines = textwrap.wrap(text=sentence, width=self.chars_per_line)

    # render a sentence into image/s of text
    def render(self):

        text_node = Text(self.lines[0], pos=self.rect.topleft, gap=(0, 10), dir=(False, True), font_color=Color('black'))
        self.text_nodes.append(text_node)

        for line in self.lines[1:len(self.lines)]:
            text_node = Text(line)
            self.text_nodes.append(text_node)
    
    def draw(self, screen):

        pygame.draw.line(screen, Color('red'), (0, ScreenCoords.four_eighths_h), (ScreenCoords.w, ScreenCoords.four_eighths_h))
        pygame.draw.line(screen, Color('red'), (ScreenCoords.four_eighths_w, 0), (ScreenCoords.four_eighths_w, ScreenCoords.h))

        pygame.draw.rect(screen, Color('black'), self.rect.inflate(10, 10), border_radius=3)
        pygame.draw.rect(screen, Color('white'), self.rect, border_radius=1)

        for text_node in self.text_nodes:
            text_node.draw(screen)

# TextPokemon is the battle stats of pokemon during a battle
# pokemon_traits consists of [name, level, health, xp]
# user can ONLY be 'enemy' or 'player'
class TextPokemon(Node):

    def __init__(self, pokemon_traits, user, **kwargs):
        super().__init__(**kwargs)
        self.pokemon_traits = pokemon_traits
        self.user = user

        if self.user == 'player':
            self.rect = pygame.Rect(ScreenCoords.one_eighth_w, ScreenCoords.two_eighths_h, ScreenCoords.two_eighths_w, ScreenCoords.three_eighths_h)
        elif self.user == 'enemy':
            self.rect = pygame.Rect(ScreenCoords.five_eighths_w, ScreenCoords.one_eighth_h, ScreenCoords.two_eighths_w, ScreenCoords.three_eighths_h)

    def draw(self, screen):
        
        pygame.draw.rect(screen, Color('white'), self.rect)
        text = Text(self.user, pos=self.rect.topleft)
        text.draw(screen)
        '''
        if self.user == 'enemy':
            #pygame.draw.line(screen, Color('black'), (ScreenCoords.two_eighths_w, 0), (ScreenCoords.two_eighths_w, ScreenCoords.h))
        else:
            #pygame.draw.line(screen, Color('black'), (ScreenCoords.six_eighths_w, 0), (ScreenCoords.six_eighths_w, ScreenCoords.h))
        '''



'''
# Indicator displays text with values that need to be updated periodically
# To init, pass text with formating e.g '{} x {} - {}'
# pass values as an list even if one element e.g [1], [1, 2, 3]
# pass max amt the value can be e.g 0-999 pass 999
class Indicator(Node):

    def __init__(self, text, values, max_amt **kwargs):
        super().__init__(**kwargs)

        self.text = text
        self.values = values
        self.max_amt = max_amt

        self.font_name = None
        self.font_size = 48
        self.font_color = pygame.Color('white')

    def set_font(self):
        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.font_size = self.font.size()
        Node.size = self.font_size

    def update_value(self, values):

        if len(values) > 1:
            self.display_text = self.text.format(values[0], values[1])
        else:
            self.display_text = self.text.format(values[0])

        self.render()

    def render(self):
        self.image = self.font.render(self.display_text)


'''


class TextButton(Node):

    types = {'text-main': (500, 1), 'selection-main': 2, 'selection-side': 3}

    def __init__(self, text, type, **kwargs):
        super().__init__(**kwargs)

        self.node_size = (0, 0)
        for ntype in TextButton.types.keys():
            if ntype == type:
                self.type = type
                self.node_size = TextButton.types[type]

        self.images = []
        self.rects = []

        self.text = text

        self.font_name = None
        self.font_size = 48
        self.font_color = pygame.Color('black')

        self.set_font()
        self.word_wrap()
        self.render()

        self.child_update()

    def word_wrap(self):

        char_per_line = self.node_size[0]//self.font_size_per_char[0]
        lines = []
        line = []
        print(char_per_line)
        print(len(self.text))
        for i in range(0, len(self.text)):
            if (i+1)%char_per_line == 0 or i == len(self.text)-1:
                line.append(self.text[i])
                lines.append(line)
                line = []
            else:
                line.append(self.text[i])

        self.lines = lines
        
    def set_font(self):
        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.font_size_per_char = self.font.size('A')
        Node.size = self.node_size

    def render(self):
        pos = Node.pos
        y_offset = self.font_size_per_char[1]
        for line in self.lines:
            text_line = ''.join([str(char) for char in line])
            #print(text_line)
            image = self.font.render(text_line, True, self.font_color)
            self.images.append(image)
            rect = image.get_rect()
            self.rects.append(rect)
            rect.topleft = pos

            pos = (pos[0], pos[1]+y_offset)

    def draw(self, screen):
        for i in range(0, len(self.images)):
            pygame.draw.rect(screen, pygame.Color('white'), self.rects[i])
            screen.blit(self.images[i], self.rects[i])

        
        


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

class Node:

    id = 0

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

# just an easier way to group nodes based on some game feature
# give a str name for checking later
class Group:
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes

    def add_nodes(self, nodes):
        for node in nodes:
            self.nodes.append(node)

    def get_name(self):
        return self.name

    def draw(self, screen):
        for node in self.nodes:
            node.draw(screen)

# text node displays text to scene
# text node is sized based on its contents and fontsize
class Text(Node):
    
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)

        self.text = text

        self.font_name = None
        self.font_size = 48
        self.font_color = pygame.Color('white')

        self.set_font()
        self.render()

        self.child_update()

    def set_font(self):
        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.font_size = self.font.size(self.text)
        Node.size = self.font_size
    
    def render(self):
        self.image = self.font.render(self.text, True, self.font_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = Node.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

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

        
        


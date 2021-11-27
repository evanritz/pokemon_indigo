import pygame
from pygame.locals import *

class Mouse:

    def __init__(self):

        self.LEFT = False
        self.MIDDLE = False
        self.RIGHT = False

    def get_pos(self):
        return pygame.mouse.get_pos()
    
    def reset_buttons(self):
        self.LEFT = False
        self.MIDDLE = False
        self.RIGHT = False

    def get_buttons(self):
        
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.MOUSEBUTTONDOWN:

                buttons = pygame.mouse.get_pressed(num_buttons=3)
                print(self.LEFT)
                self.LEFT = buttons[0]
                self.MIDDLE = buttons[1]
                self.RIGHT = buttons[2]
                print(self.LEFT)

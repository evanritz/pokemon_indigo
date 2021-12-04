# keyboard.py
#
#
# Get player key input
# Clear inst vars
# Set inst vars respectively
#
# Written by Evan


import pygame
from pygame.locals import *
from consts import *

class Input:

    def __init__(self):
    
        # direction key bools
        self.UP, self.DOWN, self.LEFT, self.RIGHT = False, False, False, False

        # special key bools
        self.SHIFT, self.SPACE = False, False

        # action key bools
        self.SELECT, self.INCREMENT, self.HEAL = False, False, False

        # game status bools
        self.PAUSE_GAME, self.EXIT_GAME = False, False

        self.M_LEFT, self.M_MIDDLE, self.M_RIGHT = False, False, False

    def get_pos(self):
        return pygame.mouse.get_pos()

    # resets key bools
    def reset_bools(self):
        self.UP, self.DOWN, self.LEFT, self.RIGHT = False, False, False, False
        self.SHIFT, self.SPACE = False, False
        self.SELECT, self.INCREMENT, self.HEAL = False, False, False
        self.PAUSE_GAME, self.EXIT_GAME = False, False
        self.M_LEFT, self.M_MIDDLE, self.M_RIGHT = False, False, False

    # get key events, compare keybinds and set inst vars
    def get_events(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.EXIT_GAME = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.PAUSE_GAME = True
                elif event.key == K_w:
                    self.UP = True
                elif event.key == K_a:
                    self.LEFT = True
                elif event.key == K_s:
                    self.DOWN = True
                elif event.key == K_d:
                    self.RIGHT = True
                elif event.key == K_LSHIFT:
                    self.SHIFT = True
                elif event.key == K_SPACE:
                    self.SPACE = True
                elif event.key == K_l:
                    self.SELECT = True
                elif event.key == K_i:
                    self.INCREMENT = True
                elif event.key == K_h:
                    self.HEAL = True
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.PAUSE_GAME = False
                elif event.key == K_w:
                    self.UP = False
                elif event.key == K_a:
                    self.LEFT = False
                elif event.key == K_s:
                    self.DOWN = False
                elif event.key == K_d:
                    self.RIGHT = False
                elif event.key == K_LSHIFT:
                    self.SHIFT = False
                elif event.key == K_SPACE:
                    self.SPACE = False
                elif event.key == K_l:
                    self.SELECT = False
                elif event.key == K_i:
                    self.INCREMENT = False
                elif event.key == K_h:
                    self.HEAL = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.M_LEFT = True
                elif event.button == 2:
                    self.M_MIDDLE = True
                elif event.button == 3:
                    self.M_RIGHT = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.M_LEFT = False
                elif event.button == 2:
                    self.M_MIDDLE = False
                elif event.button == 3:
                    self.M_RIGHT = False




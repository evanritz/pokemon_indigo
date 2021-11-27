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

class Keyboard:

    def __init__(self):
    
        # direction key bools
        self.UP, self.DOWN, self.LEFT, self.RIGHT = False, False, False, False

        # special key bools
        self.SHIFT, self.SPACE = False, False

        # action key bools
        self.SELECT, self.INCREMENT = False, False

        # game status bools
        self.PAUSE_GAME, self.EXIT_GAME = False, False

        # Raw keys 
        # direction key bools
        self.R_UP, self.R_DOWN, self.R_LEFT, self.R_RIGHT = False, False, False, False

        # special key bools
        self.R_SHIFT, self.R_SPACE = False, False

        # action key bools
        self.R_SELECT, self.R_INCREMENT = False, False

        self.MOUSELEFT = False

        self.t1, self.t0 = pygame.time.get_ticks(), pygame.time.get_ticks()

    def get_motion_keys(self):
        return [self.UP, self.LEFT, self.DOWN, self.RIGHT]

    # resets key bools
    def reset_keys(self):
        self.UP, self.DOWN, self.LEFT, self.RIGHT = False, False, False, False
        self.SHIFT, self.SPACE = False, False
        self.SELECT, self.INCREMENT = False, False
        self.PAUSE_GAME, self.EXIT_GAME = False, False

        self.MOUSELEFT = False

    # get key events, compare keybinds and set inst vars
    def get_key_events(self):

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
            elif event.type == MOUSEBUTTONDOWN:
                self.MOUSELEFT = True



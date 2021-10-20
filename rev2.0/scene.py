import pygame
import os

from pygame.locals import *
from boxes import EnemyBox, PlayerBox, InfoBox
from states import AppStates

from keybinds import *
from consts import *
from dirs import *

class Scene:

    def __init__(self, state, next_states):

        # the state of the scene
        # states of scenes that this scene can transtion to
        self.state = state
        self.next_states = next_states

        self.rez = SCREEN_REZ

        # TODO: update keybinds.py and pull from there

        if self.state == AppStates.game:
            self.keybinds = GAME_KEYBINDS
        elif self.state == AppStates.battle:
            self.keybinds = BATTLE_KEYBINDS
        elif self.state == AppStates.text:
            self.keybinds = TEXT_KEYBINDS
        elif self.state == AppStates.start:
            self.keybinds = MENU_KEYBINDS

        self.game = None

        self.bg_image = None

        self.flag = None

        self.boxes = []

    def do_keybinds(self, type, event):
        key = event.key
        mod = event.mod
        if type == KEYDOWN:# and 'down' in self.keybinds.keys():
            if (key, mod) in self.keybinds['down']:
                print('up')
                exec(self.keybinds['down'][key, mod])
        elif type == KEYUP and 'up' in self.keybinds.keys():
            if (key, mod) in self.keybinds['up']:
                print('down')
                exec(self.keybinds['up'][key, mod])

    # flag = scene name or none
    def check_flag(self):
        return self.flag

    def transtion(self, idx):
        self.flag = self.next_states[idx]

    def get_state(self):
        return self.state

    # Only one scene will have a game object
    def add_game(self, game):
        self.game = game

    def add_box(self, box):
        self.boxes.append(box)
    
    def set_resolution(self, rez):
        self.rez = rez

    def set_bg(self, file_name):
        self.bg_image = pygame.image.load(os.path.join(GAME_BGS_DIR, file_name))
        self.bg_image = pygame.transform.scale(self.bg_image, self.rez)

    def update(self):
        self.game.update()
    
    def draw(self, screen):
        
        #print(self.flag)

        if self.bg_image != None:
            screen.blit(self.bg_image, self.bg_image.get_rect())

        for box in self.boxes:
            box.draw(screen)

        if self.game != None:
            self.game.draw(screen)



    

    
    
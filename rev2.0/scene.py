import pygame
import os

from pygame.locals import *
from boxes import EnemyBox, PlayerBox, InfoBox
from states import AppStates

from keybinds import *
from consts import *
from dirs import *

class Scene:

    def __init__(self, state):

        # the state of the scene
        # states of scenes that this scene can transtion to
        self.state = state

        self.rez = SCREEN_REZ

        if self.state == AppStates.game:
            self.next_states = {'battle': AppStates.battle, 'text': AppStates.text}
            self.keybinds = GAME_KEYBINDS
        elif self.state == AppStates.battle:
            self.next_states = {'game': AppStates.game, 'text': AppStates.text}
            self.keybinds = BATTLE_KEYBINDS
        elif self.state == AppStates.text:
            self.next_states = {'game': AppStates.game, 'battle': AppStates.battle}
            self.keybinds = TEXT_KEYBINDS
        elif self.state == AppStates.start:
            self.next_states = {'battle': AppStates.game, 'text': AppStates.text}
            self.keybinds = MENU_KEYBINDS

        self.game = None

        self.bg_image = None

        self.flag = None

        self.boxes = []

    def get_keybinds(self):
        return self.keybinds

    def do_keybinds(self, type, event):
        key = event.key
        mod = event.mod
        if type == KEYDOWN:# and 'down' in self.keybinds.keys():
            if (key, mod) in self.keybinds['down']:
                exec(self.keybinds['down'][key, mod])
        elif type == KEYUP and 'up' in self.keybinds.keys():
            if (key, mod) in self.keybinds['up']:
                exec(self.keybinds['up'][key, mod])

    # flag = scene name or none
    def check_flag(self):
        flag = self.flag
        self.flag = None
        return flag

    def transtion(self, key):
        
        if key != None:

            self.flag = self.next_states[key]

    def get_state(self):
        return self.state

    # Only one scene will have a game object
    def add_game(self, game):
        self.game = game

    def add_box(self, box):
        self.boxes.append(box)

    def get_boxes(self):
        return self.boxes
    
    def set_resolution(self, rez):
        self.rez = rez

    def set_bg(self, file_name):
        self.bg_image = pygame.image.load(os.path.join(GAME_BGS_DIR, file_name))
        self.bg_image = pygame.transform.scale(self.bg_image, self.rez)

    def game_update(self):
        self.game.update()

        if self.game.check_flag() != None:
            self.transtion(self.game.check_flag())

    def non_game_update(self):
        self.transtion(self.boxes[0].check_flag())
    
    def draw(self, screen):

        if self.bg_image != None:
            screen.blit(self.bg_image, self.bg_image.get_rect())

        for box in self.boxes:
            box.draw(screen)

        if self.game != None:
            self.game.draw(screen)



    

    
    
'''
app.py 

This file contians the main function

rev1.0 - 9/16/21
Inplementing Scene Class for loading of backgrounds
Implementing Node Class and Clid Classes (Text, Button, TextButton, StatusBar, Indicator)

App holds a list of Scenes
Scenes hold a list of Nodes
App calls Scene to draw itself and Nodes

App <- Scene <- Nodes

Written by Evan

'''

import os
import pygame
import random
# imports constants from pygame so no need for pygame.constant reference
from pygame.locals import *

# importing Scene from local dir
from scene import Scene
from consts import *
from states import AppStates
from boxes import EnemyBox, PlayerBox, Text, InfoBox
from game import Game

class App:

    # version control to change every revison 
    game_name = 'Pokemon Indigo'
    
    def __init__(self):
        # create empty scenes dict and empty current scene
        self.scenes = {}
        self.scene = None

        self.clock = pygame.time.Clock()
        self.fps = 60

        # start pygame screen, set title, and set screen to be resizable
        pygame.init()
        pygame.display.set_caption(self.game_name)

        #pygame.key.set_repeat(200)

        # Set screen to spawn at current display res in Fullscreen mode, ESC to exit
        self.screen = pygame.display.set_mode(SCREEN_REZ)#FULLSCREEN)
        self.screen_rect = self.screen.get_rect()

        self.running = True # This is just for inital rev, will have more logic based on task (start menu, ingame menu, game, etd)

        self.game_init()

    def game_init(self):

        game = Game()

        game_scene = Scene(AppStates.game, [AppStates.battle, AppStates.text])
        game_scene.add_game(game)
        game_scene.set_bg('img5.jpg')
        self.add_scene(game_scene)

        battle_scene = Scene(AppStates.battle, [AppStates.game, AppStates.text])
        infobox = InfoBox('text', ['lol', 'yur'])
        infobox.add_moves(['Now', 'This', 'is', 'Epic'])
        battle_scene.add_box(infobox)
        battle_scene.add_box(EnemyBox())
        battle_scene.add_box(PlayerBox())
        battle_scene.set_resolution((1000, 600))
        battle_scene.set_bg('grass_battle.png')
        self.add_scene(battle_scene)

        text_scene = Scene(AppStates.text, [AppStates.battle, AppStates.text])
        text_scene.add_box(InfoBox('text', ['lol', 'm8', 'wahts up']))
        text_scene.set_bg('img1.jpg')
        self.add_scene(text_scene)

        start_menu_scene = Scene(AppStates.start, [AppStates.text, AppStates.battle])
        start_menu_scene.add_box(Text('Menu', fonttype='start_menu', postype='center', pos=self.screen_rect.center))
        start_menu_scene.set_bg('start_menu_bg.png')
        self.add_scene(start_menu_scene)

    def run(self):
        # program/game loop

        while self.running:

            # loop through events (keyboard, mouse, etc)
            for event in pygame.event.get():
                
                if event.type == QUIT: # pygame.QUIT
                    self.running = False
                
                if event.type == KEYDOWN or event.type == KEYUP:
                    self.scene.do_keybinds(event.type, event)
                '''
                elif event.type == KEYDOWN: 
                    self.scene.do_keybinds(event)
                elif event.type == KEYUP:
                    
                    if event.key == K_ESCAPE:
                        self.running = False
                '''

            if self.scene.get_state() == AppStates.game:
                self.scene.update()

            scene_flag = self.scene.check_flag()
            if  scene_flag != None:
                self.change_scene(scene_flag)

            # draw scene to screen
            self.scene.draw(self.screen)
            

            # update display every iter
            pygame.display.flip()

            self.clock.tick(self.fps)

        pygame.quit()    

    # adds a new scene to scenes dict with its name as the dict key
    def add_scene(self, scene):
        self.scene = scene
        state = self.scene.get_state()
        scene_dict = {state: self.scene}
        self.scenes.update(scene_dict)

    def change_scene(self, state):
        self.scene = self.scenes[state]

    # selection text main function


        
# main function, init App and run method
if __name__ == '__main__':
    App().run()
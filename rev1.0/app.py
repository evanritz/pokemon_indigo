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

import pygame
# imports constants from pygame so no need for pygame.constant reference
from pygame.locals import *

# importing Scene from local dir
from scene import Scene
from nodes import Text, Group, TextButton

class App:

    # version control to change every revison 
    game_name = 'Pokemon Indigo'
    game_revison = '1.0'

    # default screen resolution at startup
    default_screen_resolution = (1366, 768)

    def __init__(self):
        # create empty scenes list, empty current scene, and scene index starting at 0
        self.scenes = []
        self.scene = None
        self.scene_idx = 0

        # start pygame screen, set title, and set screen to be resizable
        pygame.init()
        pygame.display.set_caption('{}-rev{}'.format(self.game_name, self.game_revison))
        self.screen = pygame.display.set_mode(self.default_screen_resolution, RESIZABLE)

        self.running = True # This is just for inital rev, will have more logic based on task (start menu, ingame menu, game, etd)

        self.get_screen_resolution()

        print('SCREEN_RES={} SCREEN_CENTER={}'.format(self.screen_size, self.screen_center))

    def run(self):
        # program/game loop

        # this will be turning to a function where all game objects, etc will init and setup
        # change dir path on windows, this for my linux machine
        s1 = Scene(dir='/home/evan/Desktop/Pokemon_Indigo/rev1.0/imgs/', file='img1.jpg')
        t1 = [Text('Test 123', dir=(False, True), gap=(10, 10)), Text('Test 456'), Text('Test 789')]
        g1 = Group('Test Txt Group', t1)
        s1.add_node(g1)
        tb1 = TextButton('jdslkajdlkjsaldjaljdalksjdlkajdlkjaslkdjsalkjdalksjdlkasjdlkajdlksajdlkajsdlkjsadlkjsalkj', 'text-main')
        tb2 = TextButton('LOL My Name is Evan, Whats up buddy', 'text-main', pos=(0, 200))
        g2 = Group('Test TxtButt Group', [tb1, tb2])
        s1.add_node(g2)
        self.add_scene(s1)
        s2 = Scene(background=Color('green'))
        s2.add_node(TextButton('TEAM B IS THE BEST LOL MEMES OMG THIS RANDOM XD', 'text-main', pos=(0,0)))
        self.add_scene(s2)
        # pygame.Color('black') == (0, 0, 0)
        self.add_scene(Scene(background=Color('purple')))
        # notice how only the file kwarg is need to load picture, dir was saved for all objects of scene class
        self.add_scene(Scene(file='img4.jpg'))

        while self.running:

            # loop through events (keyboard, mouse, etc)
            for event in pygame.event.get():
                if event.type == QUIT: # pygame.QUIT
                    self.running = False
                # This is just for inital rev, much more logic for bindings will be added later
                # mouse right click increment throught scenes
                elif event.type == MOUSEBUTTONDOWN:
                    self.change_scene(event.button)

            # draw scene to screen
            self.scene.draw(self.screen)

            # update display every iter
            pygame.display.flip()

        pygame.quit()


    def get_screen_resolution(self):
        # get screen rect, size, and center
        self.screen_rect = self.screen.get_rect()
        self.screen_size = self.screen.get_size()
        self.screen_center = self.screen_rect.center


    def change_scene(self, button):
        # update current scene based on mouse input

        if len(self.scenes) > 1:
            if button == 3 and self.scene_idx < len(self.scenes)-1:
                self.scene_idx += 1
            else:
                self.scene_idx = 0

            self.scene = self.scenes[self.scene_idx]

    def add_scene(self, scene):
        # This function will be added on to
        # This function will have a enum passed for dict {enum.scene_type: scene}
        # adds scene to scenes
        # sets the scene to the current scene
        # increments the scene idx
        self.scenes.append(scene)
        self.scene = scene 
        self.scene_idx += 1




        
# main function, init App and run method
if __name__ == '__main__':
    App().run()
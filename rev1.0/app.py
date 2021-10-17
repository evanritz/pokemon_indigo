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
from nodes import Text, Group, TextMain, TextPokemon
from screen_grid import ScreenGrid, EnemyPokemonBox

class App:

    # version control to change every revison 
    game_name = 'Pokemon Indigo'
    game_revison = '1.0'
    game_dir = None
    
    def __init__(self):
        # create empty scenes dict and empty current scene
        self.scenes = {}
        self.scene = None

        self.clock = pygame.time.Clock()
        self.fps = 60

        # part of change_scene func, will be removed later
        self.key_idx = 0

        # start pygame screen, set title, and set screen to be resizable
        pygame.init()
        pygame.display.set_caption('{}-rev{}'.format(self.game_name, self.game_revison))
        
        # Get current screen info, res, spec, etc
        self.screen_info = pygame.display.Info()
        # Give to ScreenCoords to calc points of use
        ScreenGrid(self.screen_info)
        
        App.game_dir = os.path.abspath('.')

        # Screen res set to static for ease of access
        App.default_screen_resolution = (1000, 900) # 10:9 aspect ratio

        # Set screen to spawn at current display res in Fullscreen mode, ESC to exit
        self.screen = pygame.display.set_mode(App.default_screen_resolution)#FULLSCREEN)

        self.running = True # This is just for inital rev, will have more logic based on task (start menu, ingame menu, game, etd)

    def run(self):
        # program/game loop

        # THIS IS COMMENTED TO TEST. TO JUST RUN APP.PY UNCOMMENT THIS
        '''
        # this will be turning to a function where all game objects, etc will init and setup
        # change dir path on windows, this for my linux machine
        s1 = Scene('scene1', dir='/home/evan/Desktop/Pokemon_Indigo/src/rev1.0/imgs/', file='img1.jpg')
        t1 = [Text('Test 123', dir=(True, False), gap=(10, 10)), Text('Test 456'), Text('Test 789')]
        g1 = Group('Test Txt Group', t1)
        s1.add_node_group(g1)
        tb1 = Text('jdslkajdlkjsaldjaljdalksjdlkajdlkjaslkdjsalkjdalksjdlkasjdlkajdlksajdlkajsdlkjsadlkjsalkj', pos=(0, 500), gap=(10,10), dir=(True, False))
        tb2 = Text('LOL My Name is Evan, Whats up buddy')
        tm = TextMain(['My name is Evan','Whats up', 'sdasjdlajsdljalsdjlajdlajldsjaldjaldjlsakjdlkajdlklkfjaslkdjalkjdslksajdlkjsajdlsajdljsadlkjsalkjdlsajdlkjsad', 'Gr8 m8 I would r8 8/8'])
        pt = TextPokemon([1, 2, 4, 5], 'enemy')
        pt2 = TextPokemon([], 'player')
        g2 = Group('Test TxtButt Group', [tb1, tb2])
        s1.add_node_group(g2)
        self.add_scene(s1)
        s2 = Scene('scene2', background=Color('green'))
        s2.add_node_group(Group('main', [tm]))
        s2.add_node_group(Group('enemy', [pt]))
        s2.add_node_group(Group('player', [pt2]))
        #s2.add_node(TextButton('TEAM B IS THE BEST LOL MEMES OMG THIS RANDOM XD', 'text-main', pos=(0,0)))
        self.add_scene(s2)
        # pygame.Color('black') == (0, 0, 0)
        self.add_scene(Scene('scene3', background=Color('purple')))
        # notice how only the file kwarg is need to load picture, dir was saved for all objects of scene class
        self.add_scene(Scene('scene4', file='img4.jpg'))
        '''
        while self.running:

            # loop through events (keyboard, mouse, etc)
            for event in pygame.event.get():
                if event.type == QUIT: # pygame.QUIT
                    self.running = False
                # This is just for inital rev, much more logic for bindings will be added later
                # mouse right click increment throught scenes
                elif event.type == MOUSEBUTTONDOWN:
                    self.change_scene(event.button)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False

                    if event.key == K_SPACE:
                        scene = self.get_scene('scene4')
                        if scene == self.scene:
                            self.change_scene(1)
                    if event.key == K_e:
                        node_group = self.get_node_group('scene2', 'player')
                        main = node_group.get_nodes()[0]
                        x = [random.randint(1, 1000),random.randint(1, 999), random.randint(1, 1000), random.randint(1, 1000)]
                        main.update_vals(x)  
                        #print(main.__dict__)
                    if event.key == K_r:
                        node_group = self.get_node_group('scene2', 'enemy')
                        main = node_group.get_nodes()[0]
                        x = [random.randint(1, 100),random.randint(1, 100), random.randint(1, 1000), random.randint(1, 1000)]
                        main.update_vals(x)  
                    if event.key == K_a:
                        node_group = self.get_node_group('scene2', 'main')
                        main = node_group.get_nodes()[0]
                        s = [str(random.randint(1, 1000)), str(random.randint(1000, 10000))]
                        main.add_sentences(s)
                    
                    if event.key == K_i:
                        node_group = self.get_node_group('scene2', 'main')
                        main = node_group.get_nodes()[0]
                        main.increment_text()   

            # draw scene to screen
            self.scene.draw(self.screen)
            

            # update display every iter
            pygame.display.flip()

            self.clock.tick(self.fps)

        pygame.quit()

    # returns the scene object with given name
    # pass name of scene to return
    def get_scene(self, name):
        for scene_name, scene in self.scenes.items():
            if scene_name == name:
                return scene

    # returns the node group object from a given scene.
    # pass scene_name of scene to get node groups
    # pass name of node group to return
    def get_node_group(self, scene_name, name):
        scene = self.get_scene(scene_name)
        node_groups = scene.get_node_groups()
        for node_group_name, node_group in node_groups.items():
            if node_group_name == name:
                return node_group
        

    # changes current scene based on mouse click: +1 right, -1 left
    # This is just for inital rev for testing
    def change_scene(self, button):
        # update current scene based on mouse input
        if len(self.scenes) > 1:
            keys = list(self.scenes.keys())
            if button == 3:
                if len(self.scenes)-1 > self.key_idx:
                    self.key_idx += 1
                self.scene = self.get_scene(keys[self.key_idx])
            elif button == 1:
                if 0 < self.key_idx:
                    self.key_idx -= 1    
                self.scene = self.get_scene(keys[self.key_idx])

    def decrement_scene(self):
        curr_scene = self.scene.get_name()
        

    # adds a new scene to scenes dict with its name as the dict key
    def add_scene(self, scene):
        # gets scene name
        # creates a len=1 dict and adds to scenes dict
        scene_name = scene.get_name()
        scene_dict = {scene_name: scene}
        self.scene = scene
        self.scenes.update(scene_dict)

    # selection text main function


        
# main function, init App and run method
if __name__ == '__main__':
    App().run()
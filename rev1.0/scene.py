'''
scene.py

Handles background scene and nodes attached to it

Draws background img/color and all nodes

To do:
Sub classes (Menu, Transition)

rev1.0 - 9/16/21
Created base Scene Class

Written by Evan

'''

import pygame
import os

from nodes import Text

class Scene:

    # static vars, any object of this class can update these
    id = 0
    dir = None

    def __init__(self, **kwargs):
        # kwargs are keyword arguments, pass in this format: var_name=data_value

        # will hold all the different types of node groups specfic to this scene and will draw them
        self.node_groups = []
        
        # holds the file name of img for background
        self.file = None

        # sets the current id to itself and increments for the next scene
        self.id = Scene.id
        Scene.id += 1

        # represents if this scene is holding a img
        self.isImg = True

        # if dir was passed, set it. This way, dir only has to be set once
        if 'dir' in kwargs:
            Scene.dir = kwargs['dir']

        # if file was passed, set it, create the file path to it, and load it in.
        if 'file' in kwargs:
            self.file = kwargs['file']
            print(self.file, Scene.dir)
            self.file_path = os.path.join(Scene.dir, self.file)
            self.orig_img = pygame.image.load(self.file_path)
        # if no img file, set isImg to false
        else:
            self.isImg = False

        # if no img file is passed, check for a static color background
        if 'background' in kwargs:
            self.background = kwargs['background']
        # if no img file and no background default to black
        elif self.file == None:
            self.background = pygame.Color('black')

    def add_node(self, node):
        # can pass a single node or node group
        self.node_groups.append(node)

    def draw(self, screen):

        if not self.isImg:
            # fill screen with color
            screen.fill(self.background)
        else:
            # img gets scaled to screen resoultion without overwriting loaded image
            self.img = pygame.transform.smoothscale(self.orig_img, screen.get_size())
            # put on screen
            screen.blit(self.img, self.img.get_rect())

        for node in self.node_groups:
            node.draw(screen)
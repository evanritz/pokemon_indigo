# utils.py
#
# common util functions
#
# Written by Evan

import pygame
import json
import os

def load_sprite_file(file_path, file_name):
     with open(os.path.join(file_path, file_name)) as f:
        return json.loads(f.read())

def load_image_file(file_path, file_name):
    return pygame.image.load(os.path.join(file_path, file_name)).convert_alpha()

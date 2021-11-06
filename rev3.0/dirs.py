# dirs.py
#
# Creates dir paths to be System/OS independent
#
# Written by Evan

import os

GAME_DIR = os.path.abspath('.')

SPRITESHEETS_DIR = os.path.join(GAME_DIR, 'spritesheets')

TILESHEETS_DIR = os.path.join(GAME_DIR, 'tilesheets')

MAPS_DIR = os.path.join(GAME_DIR, 'maps')
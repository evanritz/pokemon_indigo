# consts.py
#
# Holds all useful constants
#
# Written by Evan

# SCREEN CONSTS
# height: 32*28 = 896
# width: 32*32 = 1024
SCREEN_H = 896
SCREEN_W = 1024
SCREEN_REZ = (SCREEN_W, SCREEN_H)

# FPS
FPS = 60

# Layer levels
FLOOR_LAYER = 1
DECOR_LAYER = 2
SHADOW_LAYER = 3
PLAYER_LEVEL = 4


# Player Movement (abs)
PLAYER_WALKING_VEL = 5
PLAYER_RUNNING_VEL = 10

# Player Sprite Size
PLAYER_SPRITE_SIZE = (128, 128)

# Animation per Frames (.1 => 1 animation / 10 frames)
APF = .15

# Map Tiles
TILE_SIZE = 64
SRC_TILE_SIZE = 16

# Map Doors
BIG_WOODEN_HOUSE_DOOR_ID = 1168
BIG_WOODEN_HOUSE_DOOR_MAP_NAME = 'test_inner.tmx'


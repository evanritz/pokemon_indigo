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

# Screen Rez 1024*896
# DS Rez 256*192
# 1024/256 = 4
# 896/192 = 4.6666 ~= 4
REZ_SCALE = 4

# FPS
FPS = 60

# Keyboard Bouncing delay (ms)
DT = 0

# Layer levels
FLOOR_LAYER = 1
DECOR_LAYER = 2
SHADOW_LAYER = 3
PLAYER_LEVEL = 4


# Player Movement (abs)
PLAYER_WALKING_VEL = 5
PLAYER_RUNNING_VEL = 10

# Player Sprite Size
PLAYER_SPRITE_SIZE = (96, 96)

# Player Origin (In Tiles)
ORIGIN = (18, 150)

# Animation per Frames (.1 => 1 animation / 10 frames)
APF = .25

# Map Tiles
TILE_SIZE = 32
SRC_TILE_SIZE = 16

# Menus
# InfoBox line offset
IBL_X_OFFSET = 30
IBL_Y_OFFSET = 20

# Encouter (5%)
ENCOUTER_PROB = .01

# Map Doors

ENTRY_ROUTES = [
    {'name': 'overworld', 'goto': True, 'check': [-1, -1], 'place': [8, 1]},
    {'name': 'house2', 'goto': False, 'check': [8, 5], 'place': [4, 1]},
    {'name': 'house2', 'goto': False, 'check': [5, 5], 'place': [5, 5]}
]

EXIT_ROUTES = [
    {'name': 'overworld', 'goto': False, 'check': [5, 0], 'place': [8, 6]},
]

BIG_WOODEN_HOUSE_DOOR_ID = 1168
BIG_WOODEN_HOUSE_DOOR_MAP_NAME = 'test_inner.tmx'

CASTLE_DOOR_ID_1 = 1293
CASTLE_DOOR_ID_2 = 1294

HOUSE_EXIT_ID=86
import pygame
from pygame.locals import *

# game keybinds
GAME_KEYBINDS_DOWN = {
    (K_w, KMOD_NONE): 'self.game.move_toggle("up")',
    (K_s, KMOD_NONE): 'self.game.move_toggle("down")',
    (K_a, KMOD_NONE): 'self.game.move_toggle("left")',
    (K_d, KMOD_NONE): 'self.game.move_toggle("right")',
}

GAME_KEYBINDS_UP = {
    (K_w, KMOD_NONE): 'self.game.move_toggle("no")',
    (K_s, KMOD_NONE): 'self.game.move_toggle("no")',
    (K_a, KMOD_NONE): 'self.game.move_toggle("no")',
    (K_d, KMOD_NONE): 'self.game.move_toggle("no")',
}

GAME_KEYBINDS = {'down': GAME_KEYBINDS_DOWN, 'up': GAME_KEYBINDS_UP}

# menu keybinds
MENU_KEYBINDS_DOWN = {
    (K_SPACE, KMOD_NONE): 'self.transtion(0)',
}

MENU_KEYBINDS = {'down': MENU_KEYBINDS_DOWN}

# text keybinds
TEXT_KEYBINDS_DOWN = {
    (K_SPACE, KMOD_NONE): 'self.transtion(0)',
}

TEXT_KEYBINDS = {'down': TEXT_KEYBINDS_DOWN}

# battle keybinds
BATTLE_KEYBINDS_DOWN = {
    (K_SPACE, KMOD_NONE): 'self.transtion(0)',
    (K_i, KMOD_NONE): 'self.boxes[0].increment_sentence()',
    (K_b, KMOD_NONE): 'self.boxes[0].set_mode("battle")',
    (K_w, KMOD_NONE): 'self.boxes[0].move_moves("up")',
    (K_s, KMOD_NONE): 'self.boxes[0].move_moves("down")',
    (K_a, KMOD_NONE): 'self.boxes[0].move_moves("left")',
    (K_d, KMOD_NONE): 'self.boxes[0].move_moves("right")',
    (K_l, KMOD_NONE): 'self.boxes[0].select_move()',
}

BATTLE_KEYBINDS = {'down': BATTLE_KEYBINDS_DOWN}
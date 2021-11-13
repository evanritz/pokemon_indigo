# pokemon.py
#
# Loads and inits Pokemon objects from .json files
# 
# Written by Evan

from utils import *
from dirs import *

import os

class Pokedex:
    def __init__(self, game):
        self.game = game
        self.pokemon = []
        # list all files in POKEMON_DIR and select only .json files
        file_names = [file_name for file_name in os.listdir(POKEMON_DIR) if file_name.lower().endswith('.json')]
        for file_name in file_names:
            JSON_pokemon = load_json_file(POKEMON_DIR, file_name)
            self.pokemon.append(Pokemon(JSON_pokemon))

class Pokemon:
    def __init__(self, JSON_pokemon):
        
        self.name = JSON_pokemon['name']
        self.type = JSON_pokemon['type']
        self.moves = JSON_pokemon['moves']
        self.stats = JSON_pokemon['stats']

        self.stats.append({'name': 'xp', 'base_stat': 0})
        self.stats.append({'name': 'level', 'base_stat': 5})

        self.dynamic_moves = self.moves
        self.dynamic_stats = self.stats

        print(self.name, self.type, self.moves, self.stats)

    # static functions
    # returns data from init

    # returns a list of move names (strings)
    # if no move names returns empty list
    def get_static_moves(self):
        move_names = []
        for move in self.moves:
            move_names.append(move['name'])
        return move_names

    # pass move name and returns move name dict
    # if move name not found returns empty dict
    def get_static_move_details(self, move_name):
        for move in self.moves:
            if move_name == move['name']:
                return move
        return {}

    # pass stat_name and returns stat val
    # if stat_name not found returns -1
    def get_static_stat_val(self, stat_name):
        for stat in self.stats:
            if stat_name == stat['name']:
                return stat['base_stat']
        return -1

    def get_dynamic_moves(self):
        move_names = []
        for move in self.dynamic_moves:
            move_names.append(move['name'])
        return move_names
    
    def get_dynamic_move_details(self, move_name):
        for move in self.dynamic_moves:
            if move_name == move['name']:
                return move
        return {}

    # for changing pp value from use
    def set_dynamic_move_val(self, move_name, move_val_key, move_val):
        for move in self.dynamic_moves:
            if move_name == move['name']:
                move[move_val_key] = move_val

    def get_dynamic_stat_val(self, stat_name):
        for stat in self.dynamic_stats:
            if stat_name == stat['name']:
                return stat['base_stat']
        return -1

    def set_dynamic_stat_val(self, stat_name, stat_val):
        for stat in self.dynamic_stats:
            if stat_name == stat['name']:
                stat['base_stat'] = stat_val
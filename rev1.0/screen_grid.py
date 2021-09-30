'''

Holds a grid system coordinates for ease of access
Mainly for placing Menus, Text Nodes, Indicator Nodes, etc

Written by Evan

'''

import pygame

class AreaGrid:

    def __init__(self, rect):
        
        AreaGrid.w = rect.w
        AreaGrid.h = rect.h

        ScreenGrid.split_16(AreaGrid)


class ScreenGrid:

    def __init__(self, screen_info):

        ScreenGrid.screen_info = screen_info

        ScreenGrid.w = ScreenGrid.screen_info.current_w
        ScreenGrid.h = ScreenGrid.screen_info.current_h

        ScreenGrid.center = (ScreenGrid.w//2, ScreenGrid.h//2)

        for i in range(1, 16):
            setattr(ScreenGrid, 'w{}'.format(i), ScreenGrid.w//16*i)
        
        for i in range(1, 16):
            setattr(ScreenGrid, 'h{}'.format(i), ScreenGrid.h//16*i)
        
        #print(ScreenGrid.__dict__)


    def split_16(_class, _inst):
        for i in range(1, 16):
            setattr(_class, 'w{}'.format(i), _inst.topleft[0]+_inst.w//16*i)
        
        for i in range(1, 16):
            setattr(_class, 'h{}'.format(i), _inst.topleft[1]+_inst.h//16*i)

        

# defined rectangle with topleft position
# setattr 1/16 of the rect
class EnemyPokemonBox(pygame.Rect):
        def __init__(self):
            super().__init__(ScreenGrid.w9, 0, ScreenGrid.w4, ScreenGrid.h6)
            ScreenGrid.split_16(EnemyPokemonBox, self)
            print(self)

class PlayerPokemonBox(pygame.Rect):
     def __init__(self):
            super().__init__(ScreenGrid.w3, ScreenGrid.h4, ScreenGrid.w4, ScreenGrid.h7)
            ScreenGrid.split_16(PlayerPokemonBox, self)
            print(self)

class MainBox(pygame.Rect):
    def __init__(self):
            super().__init__(ScreenGrid.w4, ScreenGrid.h12, ScreenGrid.w8, ScreenGrid.h3)
            ScreenGrid.split_16(MainBox, self)
            print(self)

class PokemonSelectionBox(pygame.Rect):
    pass

class BattleSelectionBox(pygame.Rect):
    def __init__(self):
            super().__init__(ScreenGrid.w4, ScreenGrid.h12, ScreenGrid.w8, ScreenGrid.h3)
            #super().__init__(ScreenGrid.w6, ScreenGrid.h11, ScreenGrid.w4, ScreenGrid.h4)
            ScreenGrid.split_16(BattleSelectionBox, self)
            print(self)

class BattleSelectionItemBox(pygame.Rect):
    def __init__(self, type):
            if type == 'topleft':
                super().__init__(BattleSelectionBox.w1, BattleSelectionBox.h2, BattleSelectionBox.w7-BattleSelectionBox.w1, BattleSelectionBox.h7-BattleSelectionBox.h1)
                ScreenGrid.split_16(BattleSelectionItemBox, self)
            elif type == 'topright':
                super().__init__(BattleSelectionBox.w9, BattleSelectionBox.h2, BattleSelectionBox.w7-BattleSelectionBox.w1, BattleSelectionBox.h7-BattleSelectionBox.h1)
                ScreenGrid.split_16(BattleSelectionItemBox, self)
            elif type == 'bottomleft':
                super().__init__(BattleSelectionBox.w1, BattleSelectionBox.h9, BattleSelectionBox.w7-BattleSelectionBox.w1, BattleSelectionBox.h7-BattleSelectionBox.h1)
                ScreenGrid.split_16(BattleSelectionItemBox, self)
            elif type == 'bottomright':
                super().__init__(BattleSelectionBox.w9, BattleSelectionBox.h9, BattleSelectionBox.w7-BattleSelectionBox.w1, BattleSelectionBox.h7-BattleSelectionBox.h1)
                ScreenGrid.split_16(BattleSelectionItemBox, self)
            print(self)
class ColoredStatusBar(pygame.Rect):
    def __init__(self):
        super().__init__(0, 0, ScreenGrid.w2, 28)
        print(self)

class Menu(pygame.Rect):
    pass

class MenuItems(pygame.Rect):
    pass

class MapBox(pygame.Rect):
    pass



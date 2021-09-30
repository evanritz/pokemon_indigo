'''
This Class holds coordinates for the screen
It will init at startup and will be acccess by basic component classes.

Written by Evan
'''

# holds 1/8 divisions of the screen for placing Nodes
class ScreenCoords:

    def __init__(self, screen_info, clock):
        
        ScreenCoords.screen_info = screen_info

        ScreenCoords.clock = clock

        ScreenCoords.h = ScreenCoords.screen_info.current_h
        ScreenCoords.w = ScreenCoords.screen_info.current_w

        # screen h divisions
        ScreenCoords.one_eighth_h = int(ScreenCoords.h*(1/8))
        ScreenCoords.two_eighths_h = 2*ScreenCoords.one_eighth_h
        ScreenCoords.three_eighths_h = 3*ScreenCoords.one_eighth_h
        ScreenCoords.four_eighths_h = 4*ScreenCoords.one_eighth_h
        ScreenCoords.five_eighths_h = 5*ScreenCoords.one_eighth_h
        ScreenCoords.six_eighths_h = 6*ScreenCoords.one_eighth_h
        ScreenCoords.seven_eighths_h = 7*ScreenCoords.one_eighth_h
        
        # screen w divisions
        ScreenCoords.one_eighth_w = int(ScreenCoords.w*(1/8))
        ScreenCoords.two_eighths_w = 2*ScreenCoords.one_eighth_w
        ScreenCoords.three_eighths_w = 3*ScreenCoords.one_eighth_w
        ScreenCoords.four_eighths_w = 4*ScreenCoords.one_eighth_w
        ScreenCoords.five_eighths_w = 5*ScreenCoords.one_eighth_w
        ScreenCoords.six_eighths_w = 6*ScreenCoords.one_eighth_w
        ScreenCoords.seven_eighths_w = 7*ScreenCoords.one_eighth_w

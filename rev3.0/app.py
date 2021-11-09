# Holds main function 

from game import Game

if __name__ == '__main__':

    # States
    # Start menu Loop -> Start Intro Loop -> (Battle or Game Loops)
    # (Battle or Game Loops) -> (Battle or Game Loops)

    g = Game()
    g.menu_init()
    while g.RUNNING:
        # Start Loops here
        if g.STATE == 1:
            pass
        elif g.STATE == 2:
            g.menu_loop()
            if g.STATE == 3:
                g.fade()

        while g.PLAYING:
            # Loops here
            if g.STATE == 3:
                g.game_loop()
            elif g.STATE == 4:
                g.battle_loop()

    g.quit()
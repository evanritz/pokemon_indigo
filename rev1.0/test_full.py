from app import App

from scene import Scene
from nodes import *

from ScreenGrid import *

class Test(App):

    def __init__(self):
        super().__init__()

        #s1 = Scene('scene1', dir='/home/evan/Desktop/Pokemon_Indigo/src/rev1.0/imgs/', file='img1.jpg')
        #t1 = [Text('Test 123', dir=(True, False), gap=(10, 10)), Text('Test 456'), Text('Test 789')]
        #g1 = Group('Test Txt Group', t1)
        #s1.add_node_group(g1)
        #tb1 = Text('dsad', pos=(0, 500), gap=(10,10), dir=(True, False))
        #tb2 = Text('LOL My Name is Evan, Whats up buddy')
        print('---THIS IS THE RECTS---')
        EnemyPokemonBox()
        PlayerPokemonBox()
        MainBox()
        BattleSelectionBox()
        BattleSelectionItemBox('topleft')
        BattleSelectionItemBox('topright')
        BattleSelectionItemBox('bottomleft')
        BattleSelectionItemBox('bottomright')
        print('--------------')

        #ts = TextSelection(['Hydro Blast', 'Memes', 'Splash', 'LOL'])

        images = [pygame.image.load('pokemon/alakazam_back_2.png'), pygame.image.load('pokemon/alakazam_front_2.png')]
        scaled_images = []
        
        scaled_images.append(pygame.transform.scale(images[0], (480, 480)))
        scaled_images.append(pygame.transform.scale(images[1], (384, 384)))


        pt = TextPokemon(scaled_images, [55, 5], ['Nhatmon', 5, 100, 120], 'enemy')
        pt2 = TextPokemon(scaled_images, [400, 500], ['Evanmon', 9001, 1000, 999], 'player')
        #ind = Indicator('x{}')
        #g2 = Group('Test TxtButt Group', [tb1, tb2])
        #s1.add_node_group(g2)
        #self.add_scene(s1)
        s2 = Scene('scene2', dir='/home/evan/Desktop/Pokemon_Indigo/src/rev1.0/imgs/', file='grass_battle.png')
        tm = TextMain(['My name is Evan','Whats up', 'sdasjdlajsdljalsdjlajdlajldsjaldjaldjlsakjdlkajdlklkfjaslkdjalkjdslksajdlkjsajdlsajdljsadlkjsalkjdlsajdlkjsad', 'Gr8 m8 I would r8 8/8'])
        
        s2.add_node_group(Group('enemy', pt))
        s2.add_node_group(Group('player', [pt2]))
        s2.add_node_group(Group('main', [tm]))
        #s2.add_node(TextButton('TEAM B IS THE BEST LOL MEMES OMG THIS RANDOM XD', 'text-main', pos=(0,0)))
        self.add_scene(s2)
        # pygame.Color('black') == (0, 0, 0)
        #self.add_scene(Scene('scene3', background=Color('purple')))
        # notice how only the file kwarg is need to load picture, dir was saved for all objects of scene class
        s4 = Scene('scene4', dir='menu_bgs/', file='start_menu_bg.png')
        tsm = TextStartMenu()
        s4.add_node_group(Group('menustart', tsm))
        self.add_scene(s4)
        


if __name__ == '__main__':
    Test().run()

from app import App

from scene import Scene
from nodes import *

class Test(App):

    def __init__(self):
        super().__init__()

        s1 = Scene('scene1', dir='/home/evan/Desktop/Pokemon_Indigo/src/rev1.0/imgs/', file='img1.jpg')
        t1 = [Text('Test 123', dir=(True, False), gap=(10, 10)), Text('Test 456'), Text('Test 789')]
        g1 = Group('Test Txt Group', t1)
        s1.add_node_group(g1)
        tb1 = Text('jdslkajdlkjsaldjaljdalksjdlkajdlkjaslkdjsalkjdalksjdlkasjdlkajdlksajdlkajsdlkjsadlkjsalkj', pos=(0, 500), gap=(10,10), dir=(True, False))
        tb2 = Text('LOL My Name is Evan, Whats up buddy')
        tm = TextMain(['My name is Evan','Whats up', 'sdasjdlajsdljalsdjlajdlajldsjaldjaldjlsakjdlkajdlklkfjaslkdjalkjdslksajdlkjsajdlsajdljsadlkjsalkjdlsajdlkjsad', 'Gr8 m8 I would r8 8/8'])
        pt = TextPokemon([1, 2, 4, 5], 'enemy')
        pt2 = TextPokemon([], 'player')
        g2 = Group('Test TxtButt Group', [tb1, tb2])
        s1.add_node_group(g2)
        self.add_scene(s1)
        s2 = Scene('scene2', background=Color('green'))
        s2.add_node_group(Group('main', [tm]))
        s2.add_node_group(Group('enemy', [pt]))
        s2.add_node_group(Group('player', [pt2]))
        #s2.add_node(TextButton('TEAM B IS THE BEST LOL MEMES OMG THIS RANDOM XD', 'text-main', pos=(0,0)))
        self.add_scene(s2)
        # pygame.Color('black') == (0, 0, 0)
        self.add_scene(Scene('scene3', background=Color('purple')))
        # notice how only the file kwarg is need to load picture, dir was saved for all objects of scene class
        self.add_scene(Scene('scene4', file='img4.jpg'))


if __name__ == '__main__':
    Test().run()

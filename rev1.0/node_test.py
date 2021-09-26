'''

This is a test template for validation testing
Place all testing lines in the __init__ function
Copy this template for your testing.

Written by Evan

'''

# NODE GROUP AND NODE TEST

from app import App

from scene import *
from nodes import *

class Test(App):

    def __init__(self):
        super().__init__()

        # Create a scene with img1.jpg
        # Change dir for windows machine path
        # dir = 'path to directory with images' = string
        # file = 'file name of image file' = string
        s1 = Scene('Scene1', dir='imgs/', file='img1.jpg')
        

        # Create a scene with static blue background
        s2 = Scene('Scene2', background=Color('blue'))

        # Create a scene with img2.jpg without passing dir
        s3 = Scene('Scene3', file='img2.jpg')

        # Create Text Node thats siblings grow on the X axis
        # dir = (Move in X Direction?, Move in Y Direction?) = (bool, bool)
        # gap = (amount of gap distance in X Direction, amount of gap distance in X Direction) = (int, int)
        t1 = Text('This is Text Node 1', dir=(True, False), gap=(10, 0))
        t2 = Text('This is Text Node 2')
        t3 = Text('This is Text Node 3')
        # Create Node Group, pass Node Group name and  list of Text Nodes 
        g1 = Group('Node Group 1', [t1, t2, t3])
        # Add g1 Node Group to s3 Scene
        s3.add_node_group(g1)

        # Create Text Node thats siblings grow on the Y axis
        t4 = Text('This is Text Node 4', dir=(False, True), gap=(0, 10))
        t5 = Text('This is Text Node 5')
        t6 = Text('This is Text Node 6')

        # Create Node Group
        g2 = Group('Node Group 2', [t4, t5, t6])
        s2.add_node_group(g2)

        # Add scene 1 to scenes dict
        self.add_scene(s1)
        self.add_scene(s2)
        self.add_scene(s3)



if __name__ == '__main__':
    Test().run()




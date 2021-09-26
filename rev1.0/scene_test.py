'''

This is a test template for validation testing
Place all testing lines in the __init__ function
Copy this template for your testing.

Written by Evan

'''

# SCENE TEST

from app import App

from scene import *
from nodes import *

class Test(App):

    def __init__(self):
        super().__init__()

        # Create a scene with img1.jpg
        # Change dir for windows machine path
        s1 = Scene('Scene1', dir='imgs/', file='img1.jpg')
        # Add scene 1 to scenes dict
        self.add_scene(s1)

        # Create a scene with static blue background
        s2 = Scene('Scene2', background=Color('blue'))
        self.add_scene(s2)

        # Create a scene with img2.jpg without passing dir
        s3 = Scene('Scene3', file='img2.jpg')
        self.add_scene(s3)


if __name__ == '__main__':
    Test().run()




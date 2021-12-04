'''
cropper.py

This Program crops a given image and saves it to the local dir
Doing this to scale sprites in GIMP because pygame scale messes with texture

Argument 1 = Image file 
Argument 2 = Tuple of pos and size (x, y, w, h)

example: python cropper.py myImg.png (0, 0, 32, 32)

'''

import pygame
import sys
import os

if len(sys.argv) != 7:
    print('Pass 5 arguments to run this script.')
    print(' -arg1=img_file')
    print(' -arg2=dimensions')
    print('Exiting...')
    sys.exit()
else:
    img_file = sys.argv[1]
    dimensions = (int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))

    if os.path.exists(img_file):
        surf = pygame.Surface((dimensions[2], dimensions[3]), pygame.SRCALPHA)
        cropped_img = pygame.image.load(img_file).subsurface(dimensions)
        surf.blit(cropped_img, (0, 0))
        pygame.image.save(surf, sys.argv[6])
    else:
        print('Img file does not exist.')
        print('Exiting...')
        sys.exit()



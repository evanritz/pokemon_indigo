from dirs import PLAYER_SPRITES_DIR
import pygame
import os

from states import DirStates

class Player:

    def __init__(self, pos):

        self.pos = pos
        self.velo = 1
        self.curr_dir = [0, 0]

        self.sprite_size = (24, 24)

        self.prev_dir = 'up'

        self.x_displacement = 0
        self.y_displacement = 0

        self.delay = 100

        self.moving_toggle = False
        
        self.curr_ms = pygame.time.get_ticks()

        self.prev_ms = 0

        self.image_up = [
            pygame.transform.scale(pygame.image.load(os.path.join(PLAYER_SPRITES_DIR, 'player_up_1.png')), self.sprite_size),
            pygame.transform.scale(pygame.image.load(os.path.join(PLAYER_SPRITES_DIR, 'player_up_2.png')), self.sprite_size),
            pygame.transform.scale(pygame.image.load(os.path.join(PLAYER_SPRITES_DIR, 'player_up_3.png')), self.sprite_size)
        ]

        self.image_down = [
            pygame.transform.scale(pygame.image.load(os.path.join(PLAYER_SPRITES_DIR, 'player_down_1.png')), self.sprite_size),
            pygame.transform.scale(pygame.image.load(os.path.join(PLAYER_SPRITES_DIR, 'player_down_2.png')), self.sprite_size),
            pygame.transform.scale(pygame.image.load(os.path.join(PLAYER_SPRITES_DIR, 'player_down_3.png')), self.sprite_size)
        ]

        self.image_left = [
            pygame.transform.scale(pygame.image.load(os.path.join(PLAYER_SPRITES_DIR, 'player_left_1.png')), self.sprite_size),
            pygame.transform.scale(pygame.image.load(os.path.join(PLAYER_SPRITES_DIR, 'player_left_2.png')), self.sprite_size),
            pygame.transform.scale(pygame.image.load(os.path.join(PLAYER_SPRITES_DIR, 'player_left_3.png')), self.sprite_size)
        ]

        self.image_right = [
            pygame.transform.scale(pygame.image.load(os.path.join(PLAYER_SPRITES_DIR, 'player_right_1.png')), self.sprite_size),
            pygame.transform.scale(pygame.image.load(os.path.join(PLAYER_SPRITES_DIR, 'player_right_2.png')), self.sprite_size),
            pygame.transform.scale(pygame.image.load(os.path.join(PLAYER_SPRITES_DIR, 'player_right_3.png')), self.sprite_size)
        ]

        self.frame_buffer = {'inmotion': False, 'frames': self.image_up}

        self.frames = [] # (frame image, frame rect)

        self.frame = None # (frame image, frame rect)

        self.frame_idx = 0

        self.render()

        #self.

    def move_toggle(self, dir):
        if dir == 'up':
            self.curr_dir = [0, -1]
        elif dir == 'down':
            self.curr_dir = [0, 1]
        elif dir == 'left':
            self.curr_dir = [-1, 0]
        elif dir == 'right':
            self.curr_dir = [1, 0]
        else:
            self.curr_dir = [0, 0]

        self.prev_dir = dir

        self.moving_toggle = not self.moving_toggle

        
    def update(self):

        self.x_displacement = self.curr_dir[0]#*self.velo*self.sprite_size[0]
        self.y_displacement = self.curr_dir[1]#*self.velo*self.sprite_size[1]

        if self.moving_toggle:

            self.pos = (int(self.pos[0] + self.x_displacement), int(self.pos[1] + self.y_displacement))

            print('pos: {} dir: {} inmotion?: {} movingtoggle: {}'.format(self.pos, self.curr_dir, self.frame_buffer['inmotion'], self.moving_toggle))

            if self.x_displacement != 0:
                self.frame_buffer['inmotion'] = True
                # postive x change
                if self.x_displacement == abs(self.x_displacement):
                    # {'inmotion': False, 'frames': self.image_right}
                    self.frame_buffer['frames'] = self.image_right
                # negative x change
                elif self.x_displacement != abs(self.x_displacement):
                    self.frame_buffer['frames'] = self.image_left
            elif self.y_displacement != 0:
                self.frame_buffer['inmotion'] = True
                # postive y change
                if self.y_displacement != abs(self.y_displacement):
                    self.frame_buffer['frames'] = self.image_up
                # negative y change
                elif self.y_displacement == abs(self.y_displacement):
                    self.frame_buffer['frames'] = self.image_down

        else:
            if self.x_displacement == 0 and self.y_displacement == 0:
                self.frame_buffer['inmotion'] = False
                '''
                if self.prev_dir == 'up':
                    self.frame_buffer['frames'] = self.image_up
                elif self.prev_dir == 'down':
                    self.frame_buffer['frames'] = self.image_down
                elif self.prev_dir == 'left':
                    self.frame_buffer['frames'] = self.image_left
                elif self.prev_dir == 'right':
                    self.frame_buffer['frames'] = self.image_right
                '''
        # no chage
        #print('moving toggle: {}'.format(self.moving_toggle))
        
        
        self.render()
    
    def render(self):

        self.frames = []
        for i in range(0, len(self.frame_buffer['frames'])):
            frame = self.frame_buffer['frames'][i]
            frame_rect = frame.get_rect()
            self.frames.insert(i, (frame, frame_rect))
        
        print(len(self.frames))

        self.curr_ms = pygame.time.get_ticks()
        print(self.frame_buffer['inmotion'])
        if self.frame_buffer['inmotion']:
            if self.curr_ms-self.prev_ms >= self.delay:
                self.prev_ms = self.curr_ms
                
                if self.frame_idx < len(self.frames)-1:
                    self.frame_idx += 1
                else:
                    self.frame_idx = 0

            self.frame = self.frames[self.frame_idx]
            
        else:
            self.frame = self.frames[0]


    def draw(self, screen):
        
        #self.render()
        self.frame[1].center = self.pos
        screen.blit(self.frame[0], self.frame[1])
        




    

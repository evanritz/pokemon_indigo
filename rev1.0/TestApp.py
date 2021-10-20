
import pygame
import os

from consts import *
from dirs import *

from boxes import EnemyBox, InfoBox, PlayerBox, Text, Blinker

pygame.init()
screen = pygame.display.set_mode(SCREEN_REZ)

running = True

'''
infobox_rect = pygame.Rect(INFOBOX_TOPLEFT[0], INFOBOX_TOPLEFT[1], INFOBOX_W, INFOBOX_H)

infobox_graphic = pygame.image.load(os.path.join(MENU_TEXTURES_DIR, 'canvas.png'))
infobox_graphic = pygame.transform.scale(infobox_graphic, (INFOBOX_W, INFOBOX_H))
infobox_graphic_rect = infobox_graphic.get_rect()
infobox_graphic_rect.topleft = INFOBOX_TOPLEFT
'''
enemybox_rect = pygame.Rect(ENEMYBOX_TOPLEFT[0], ENEMYBOX_TOPLEFT[1], ENEMYBOX_W, ENEMYBOX_H)
playerbox_rect = pygame.Rect(PLAYERBOX_TOPLEFT[0], PLAYERBOX_TOPLEFT[1], PLAYERBOX_W, PLAYERBOX_H)

playerbox_sprite_rect = pygame.Rect(PLAYERBOX_SPRITE_TOPLEFT[0], PLAYERBOX_SPRITE_TOPLEFT[1], PLAYERBOX_SPRITE_W, PLAYERBOX_SPRITE_H)
playerbox_info_rect = pygame.Rect(PLAYERBOX_INFO_TOPLEFT[0], PLAYERBOX_INFO_TOPLEFT[1], PLAYERBOX_INFO_W, PLAYERBOX_INFO_H)

enemybox_sprite_rect = pygame.Rect(ENEMYBOX_SPRITE_TOPLEFT[0], ENEMYBOX_SPRITE_TOPLEFT[1], ENEMYBOX_SPRITE_W, ENEMYBOX_SPRITE_H)
enemybox_info_rect = pygame.Rect(ENEMYBOX_INFO_TOPLEFT[0], ENEMYBOX_INFO_TOPLEFT[1], ENEMYBOX_INFO_W, ENEMYBOX_INFO_H)

infobox_items_rect = pygame.Rect(INFOBOX_ITEMS_TOPLEFT[0], INFOBOX_ITEMS_TOPLEFT[1], INFOBOX_ITEMS_W, INFOBOX_ITEMS_H)

player_pokemon = pygame.image.load(os.path.join('pokemon', 'alakazam_back_2.png'))
player_pokemon = pygame.transform.scale(player_pokemon, (384, 384))
player_pokemon_rect = player_pokemon.get_rect()
player_pokemon_rect.center = playerbox_sprite_rect.center

enemy_pokemon = pygame.image.load(os.path.join('pokemon', 'alakazam_front_2.png'))
enemy_pokemon = pygame.transform.scale(enemy_pokemon, (192, 192))
enemy_pokemon_rect = enemy_pokemon.get_rect()
enemy_pokemon_rect.midbottom = enemybox_sprite_rect.midbottom

bg = pygame.image.load(os.path.join('/home/evan/Desktop/Pokemon_Indigo/src/rev1.0/imgs/grass_battle.png'))
bg = pygame.transform.scale(bg, (1000, 600))


'''
font = pygame.font.Font(os.path.join(FONTS_DIR, 'AtariClassicChunky-PxXP.ttf'), 24)

char_w = font.size('G')
print(char_w)

rendered_font_1 = font.render('This is a Test', True, pygame.Color('black'))
rendered_font_2 = font.render('This is a another Test', True, pygame.Color('black'))

rendered_font_rect_1 = rendered_font_1.get_rect()
rendered_font_rect_1.center = enemybox_info_rect.center

rendered_font_rect_2 = rendered_font_2.get_rect()
rendered_font_rect_2.midtop = rendered_font_rect_1.midbottom

test_text = Text('This is a test', pos=(0, 0), postype='left')
test_text_2 = Text('This is the second test', linktype='left', linker=test_text)
test_text_3 = Text('This is the third test', linktype='right', linker=test_text_2)
test_text_4 = Text('This is the fourth test', fonttype='start_menu', linktype='left', linker=test_text_3)
'''

#blinker = Blinker('', 1000)

infobox = InfoBox('text', ['lol', 'dasdasdsadsadsadasdasddsaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'afafafsafsaf', 'eadasddsadasdsad'])
infobox.add_moves(['Now', 'This', 'is', 'Epic'])
infobox.set_mode('battle')

enemybox = EnemyBox()
playerbox = PlayerBox()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                infobox.increment_sentence()
            elif event.key == pygame.K_t:
                infobox.set_mode('text')
            elif event.key == pygame.K_b:
                infobox.set_mode('battle')
            elif event.key == pygame.K_w:
                infobox.move_moves('up')
            elif event.key == pygame.K_s:
                infobox.move_moves('down')
            elif event.key == pygame.K_a:
                infobox.move_moves('left')
            elif event.key == pygame.K_d:
                infobox.move_moves('right')
            elif event.key == pygame.K_l:
                move = infobox.select_move()
                print(move)
            

    #pygame.draw.rect(screen, pygame.Color('yellow'), infobox_rect)
    pygame.draw.rect(screen, pygame.Color('red'), enemybox_rect)
    #pygame.draw.rect(screen, pygame.Color('blue'), playerbox_rect)
    pygame.draw.rect(screen, pygame.Color('blue'), playerbox_sprite_rect)
    pygame.draw.rect(screen, pygame.Color('yellow'), playerbox_info_rect)

    pygame.draw.rect(screen, pygame.Color('purple'), enemybox_sprite_rect)
    pygame.draw.rect(screen, pygame.Color('orange'), enemybox_info_rect)

    screen.blit(bg, bg.get_rect())

    screen.blit(player_pokemon, player_pokemon_rect)
    screen.blit(enemy_pokemon, enemy_pokemon_rect)

    #screen.blit(rendered_font_1, rendered_font_rect_1)
    #screen.blit(rendered_font_2, rendered_font_rect_2)

    #screen.blit(infobox_graphic, infobox_graphic_rect)

    infobox.draw(screen)
    enemybox.draw(screen)
    playerbox.draw(screen)

    '''
    test_text.draw(screen)
    test_text_2.draw(screen)
    test_text_3.draw(screen)
    test_text_4.draw(screen)
    '''
    #pygame.draw.rect(screen, pygame.Color('lightyellow'), infobox_items_rect)

    #blinker.update()
    #blinker.draw(screen)

    pygame.display.flip()
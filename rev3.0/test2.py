import pygame

pygame.init()
screen = pygame.display.set_mode((100, 100))

surf1 = pygame.Surface((25, 25))
surf1.fill(pygame.Color('red'))
surf2 = pygame.Surface((50, 50))
surf2.fill(pygame.Color('blue'))
surf3 = pygame.Surface((75, 75))
surf3.fill(pygame.Color('white'))

running = True

surf2.blit(surf1, surf1.get_rect())
surf3.blit(surf2, surf2.get_rect())
screen.blit(surf3, surf3.get_rect())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

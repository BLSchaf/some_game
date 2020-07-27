import pygame
import sys
import os


# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 400

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((SIZE))
pygame.display.set_caption('Something')

IMG = pygame.image.load(os.path.join('assets', 'IMG.png'))

menu_font = pygame.font.SysFont('Matura MT Script Capitals', 60, 1)
menu_label = menu_font.render('Some Menu Title', False, (0,0,0))
WINDOW.blit(menu_label, (130, round(HEIGHT*.33)))


# Loop -------------------------------------------------------- #
while True:

    # Background ---------------------------------------------- #
    WINDOW.fill((0,0,0))

    # Buttons n stuff ----------------------------------------- #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: # event has no key attribute
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_d]:
        pass
    
    # Update window ------------------------------------------- #
    pygame.display.update()
    main_clock.tick(FPS)
    
    
# Close Pygame ------------------------------------------------ #
pygame.quit()
sys.exit()

import pygame


pygame.init()

pygame.mixer.music.load(r'assets\wummern.mp3')
while True:
    pygame.mixer.music.play(-1)

pygame.time.wait(10000)

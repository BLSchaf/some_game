import pygame, os

pygame.init()

if os.path.exists('assets\wummern_.wav') == True:
    print('bla')

pygame.mixer.music.load(f'assets\wummern.ogg')
pygame.mixer.music.play(-1, 0)

"""def play_music(music, pos=0, vol=0.5):
    pygame.mixer.music.set_volume(vol)
    #pygame.mixer.music.fadeout(1000)
    #pygame.mixer.music.set_pos(pos)
    pygame.mixer.music.load(f'assets\{music}')
    pygame.mixer.music.play(-1, 0)


play_music('wummern.mp3')
"""

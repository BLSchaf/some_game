import pygame
import sys
import os
import random


# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 400
CENTER = (WIDTH//2, HEIGHT//2)

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Helper Drone')

TITLE_IMG = pygame.image.load('assets\HD_title.png')
PLAY_BUTTON_UP = pygame.image.load(os.path.join('assets', 'HD_title_play_up.png')).convert()
PLAY_BUTTON_DOWN = pygame.image.load(os.path.join('assets', 'HD_title_play_down.png')).convert()

MENU_FONT = pygame.font.SysFont('Matura MT Script Capitals', 60, 1)
MENU_LABEL = MENU_FONT.render('Helper Drone v1', False, (20, 20, 20))



class Drone():
    def __init__(self, pos):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.r = 10
        self.color = (180, 180, 200)
        self.vel = 3
        self.charging = False
        self.not_charging = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] == 1:
            self.y -= self.vel
        if keys[pygame.K_s] == 1:
            self.y += self.vel
        if keys[pygame.K_a] == 1:
            self.x -= self.vel
        if keys[pygame.K_d] == 1:
            self.x += self.vel

        self.pos = (self.x, self.y)

    def draw(self):
        pygame.draw.circle(WINDOW, self.color, (self.x, self.y), self.r)

    def is_in_sight(self):
        pass


class Line():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.color = (220, 130, 80)

    def draw(self):
        pygame.draw.line(WINDOW, self.color, self.start, self.end)


class Obstacle():
    def __init__(self, points):
        self.points = points
        self.color = (220, 130, 80)

    def draw(self):
        pygame.draw.aalines(WINDOW, self.color, True, self.points, -1)



# Intersect Stuff ------------------------------------------------- #
def slope(p1, p2):
    return (p2[1] - p1[1])*1. / (p2[0] - p1[0]) # y = mx + b | m := slope
    # ZeroDivisionError Bug - what if lines are vertical/horizontal
   
def y_intercept(slope, p1):
    return p1[1] - 1.*slope * p1[0] # y = mx+b -> b = y-mb | b:= y_intercept

def intersect(line1, line2) :
    min_allowed = 1e-5   # guard against overflow
    big_value = 1e10     # use instead (if overflow would have occurred)
    m1 = slope(line1[0], line1[1])
    b1 = y_intercept(m1, line1[0])

    m2 = slope(line2[0], line2[1])
    b2 = y_intercept(m2, line2[0])

    if abs(m1 - m2) < min_allowed:
        x = big_value
    else:
        x = (b2 - b1) / (m1 - m2)
      
    y = m1 * x + b1
    #y2 = m2 * x + b2
    return (int(x),int(y))

def segment_intersect(line1, line2):
    intersection_pt = intersect(line1, line2)

    if (line1[0][0] < line1[1][0]):
        if intersection_pt[0] < line1[0][0] or intersection_pt[0] > line1[1][0]:
            return None
    else:
        if intersection_pt[0] > line1[0][0] or intersection_pt[0] < line1[1][0]:
            return None
         
    if (line2[0][0] < line2[1][0]):
        if intersection_pt[0] < line2[0][0] or intersection_pt[0] > line2[1][0]:
            return None
    else:
        if intersection_pt[0] > line2[0][0] or intersection_pt[0] < line2[1][0]:
            return None

    return intersection_pt




def play_music(music, pos=0, vol=0.5):
    pygame.mixer.music.set_volume(vol)
    #pygame.mixer.music.fadeout(1000)
    #pygame.mixer.music.set_pos(pos)
    pygame.mixer.music.load(f'assets\{music}')
    pygame.mixer.music.play(-1, pos)

def stop_music(fadeout=True):
    if fadeout:
        pygame.mixer.music.fadeout(300)
    pygame.mixer.music.stop()    
    

# Update Game Window ---------------------------------------------- #
def update_window(drone, obstacle, intersection_pt, line_of_sight=False):
    '''
    Updates the window
    drone: Drone instance
    obstacle: Line instance
    '''
    WINDOW.fill((50, 50, 50))
    
    pygame.draw.circle(WINDOW, (220, 220, 220), CENTER, 30)
    drone.draw()
    obstacle.draw()

    if not line_of_sight:
        pygame.draw.aaline(WINDOW, (220, 130, 80), drone.pos, CENTER)
        pygame.draw.circle(WINDOW, (220, 220, 220), intersection_pt, 6, 1)
    else:
        pygame.draw.aaline(WINDOW, (130, 220, 80), drone.pos, CENTER)
    
    pygame.display.update()
    

# Main Menu ------------------------------------------------------- #
def menu():
    PLAY_BUTTON_RECT = ((WIDTH-PLAY_BUTTON_UP.get_width())//2,
                        int(HEIGHT*.7),
                        PLAY_BUTTON_UP.get_width(),
                        PLAY_BUTTON_UP.get_height())
    
    run = True
    while run:
        WINDOW.blit(TITLE_IMG, (0,0))
        WINDOW.blit(MENU_LABEL, (100, int(HEIGHT*.1)))
        PLAY_BUTTON_DOWN.set_colorkey((255, 255, 255))
        PLAY_BUTTON_UP.set_colorkey((255, 255, 255))
        
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            
            if PLAY_BUTTON_RECT[0] <= pos[0] <= PLAY_BUTTON_RECT[0] + PLAY_BUTTON_RECT[2]\
               and PLAY_BUTTON_RECT[1] <= pos[1] <= PLAY_BUTTON_RECT[1] + PLAY_BUTTON_RECT[3]:
                WINDOW.blit(PLAY_BUTTON_DOWN, (PLAY_BUTTON_RECT[0], PLAY_BUTTON_RECT[1]))
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        run = False
                            
            else:                
                WINDOW.blit(PLAY_BUTTON_UP, (PLAY_BUTTON_RECT[0], PLAY_BUTTON_RECT[1]))
                        
            pygame.display.update()

    game()


# Game Loop ------------------------------------------------------- #
def game():
    drone = Drone((50, 50))
    obstacle = Obstacle([(10,10), (20,40), (50,20)])

    line_of_sight = False

    run = True
    while run:
        
        intersection_pt = segment_intersect((obstacle.points[0], obstacle.points[1]),
                                            (drone.pos, CENTER))
        if not intersection_pt:
            line_of_sight = True
        else:
            line_of_sight = False
        
        if not intersection_pt and not drone.charging:
            drone.charging = True
            drone.not_charging = False
            play_music('wummern.mp3')
            
        elif intersection_pt and not drone.not_charging:
            drone.not_charging = True
            drone.charging = False
            play_music('idle_wummern.mp3')
            
            
        # Buttons n stuff
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: # event has no key attribute
                if event.key == pygame.K_ESCAPE:
                    run = False

        # Do Stuff 
        drone.move()

        # Update window
        update_window(drone, obstacle, intersection_pt, line_of_sight)
        main_clock.tick(FPS)

    
while True:
    menu()

# Close Pygame ------------------------------------------------ #
pygame.quit()
sys.exit()

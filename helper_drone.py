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
        self.life = 10
        

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
        self.x_vel = random.randint(-10,10)/10
        self.y_vel = random.randint(-10,10)/10

    def __len__(self):
        return len(self.points)

    def move(self):
        self.x_vel *= random.randint(90,110) / 100
        self.y_vel *= random.randint(90,110) / 100
        self.points = [(i + self.x_vel, j + self.y_vel) for i, j in self.points]

    def draw(self):
        pygame.draw.polygon(WINDOW, self.color, self.points)






# Intersection Stuff ---------------------------------------------- #
def get_slope(p1, p2):
    return (p2[1] - p1[1])*1. / (p2[0] - p1[0]) # y = mx + b | m := slope
    # ZeroDivisionError Bug - what if lines are vertical/horizontal
   
def get_y_intercept(slope, p1):
    return p1[1] - 1.*slope * p1[0] # y = mx+b -> b = y-mb | b:= y_intercept

def calc_intersect(line1, line2) :
    min_allowed = 1e-5   # guard against overflow
    big_value = 1e10     # use instead (if overflow would have occurred)

    try:
        m1 = get_slope(line1[0], line1[1])
    except ZeroDivisionError:
        m1 = big_value
        
    b1 = get_y_intercept(m1, line1[0])

    try:
        m2 = get_slope(line2[0], line2[1])
    except ZeroDivisionError:
        m2 = big_value
        
    b2 = get_y_intercept(m2, line2[0])

    if abs(m1 - m2) < min_allowed:
        x = big_value
    else:
        x = (b2 - b1) / (m1 - m2)
      
    y = m1 * x + b1
    #y2 = m2 * x + b2
    return (int(x),int(y))


def get_intersection(line1, line2):
    intersection_pt = calc_intersect(line1, line2)

    if (line1[0][0] < line1[1][0]):
        if intersection_pt[0] <= line1[0][0] or intersection_pt[0] >= line1[1][0]:
            return None
    else:
        if intersection_pt[0] >= line1[0][0] or intersection_pt[0] <= line1[1][0]:
            return None
         
    if (line2[0][0] < line2[1][0]):
        if intersection_pt[0] <= line2[0][0] or intersection_pt[0] >= line2[1][0]:
            return None
    else:
        if intersection_pt[0] >= line2[0][0] or intersection_pt[0] <= line2[1][0]:
            return None

    return intersection_pt


def update_interaction(intersection_pt, drone):   
    if not intersection_pt:
        if drone.life >= 0.1:
            drone.life -= 0.1
        else:
            #play some music?
            return False
            
    else:
        if drone.life <= 99.9:
            drone.life += 0.1
    
    if not intersection_pt and not drone.charging:
        drone.charging = True
        drone.not_charging = False
        play_music('wummern.mp3')
        
    elif intersection_pt and not drone.not_charging:
        drone.not_charging = True
        drone.charging = False
        play_music('idle_wummern.mp3')

    return True


def check_intersection(obstacles, drone):
    for obstacle in obstacles:
            for i in range(len(obstacle)):
                intersection_pt = get_intersection((obstacle.points[i],
                                                    obstacle.points[(i+1)%(len(obstacle))]),
                                                   (drone.pos, CENTER))
                
                if intersection_pt:
                    return intersection_pt
                
    return None


# Music Stuff ----------------------------------------------------- #

def play_music(music, pos=0, vol=0.5):
    pygame.mixer.music.set_volume(vol)
    #pygame.mixer.music.fadeout(1000)
    #pygame.mixer.music.set_pos(pos)
    pygame.mixer.music.load(f'assets\{music}')
    pygame.mixer.music.play(-1, pos)
    

def stop_music(fadeout=False):
    if fadeout:
        pygame.mixer.music.fadeout(300)
    else:
        pygame.mixer.music.stop()    
    

# Update Game Window ---------------------------------------------- #
def update_window(drone, obstacles, intersection_pt):
    '''
    Updates the window
    drone: Drone instance
    obstacle: Line instance
    '''
    WINDOW.fill((50, 50, 50))
    
    pygame.draw.circle(WINDOW, (220, 220, 220), CENTER, 30)

    pygame.draw.rect(WINDOW, (80,80,80), (WIDTH - 122, 18, 104, 24))
    pygame.draw.rect(WINDOW, (220, 220, 220), (WIDTH - 120, 20, int(drone.life), 20))
    
    drone.draw()
    for obstacle in obstacles:
        obstacle.draw()

    if intersection_pt:
        pass
        #pygame.draw.aaline(WINDOW, (220, 130, 80), drone.pos, CENTER)
        #pygame.draw.circle(WINDOW, (220, 220, 220), intersection_pt, 6, 1)
    else:
        pygame.draw.aaline(WINDOW, (130, 220, 80), drone.pos, CENTER)
    
    pygame.display.update()

    

# Main Menu ------------------------------------------------------- #
def menu():
    PLAY_BUTTON_RECT = ((WIDTH-PLAY_BUTTON_UP.get_width())//2,
                        int(HEIGHT*.7),
                        PLAY_BUTTON_UP.get_width(),
                        PLAY_BUTTON_UP.get_height())

    LEVEL_DICT = {
        1: [Drone((50, 50)),
            []
        ],
        2: [Drone((50, 50)),
            [
            Obstacle([(50,50), (50,100), (120,70), (130,50)]),
            Obstacle([(100,130), (120,160), (130,150)])
            ]
        ],
        3: [Drone((50, 50)),
            [
                Obstacle([(50,50), (50,100), (120,70), (130,50)]),
                Obstacle([(100,130), (120,160), (130,150)]),
                Obstacle([(400,230), (500,250), (520, 200), (480, 180), (430, 200)])
            ]
        ]             
    }
    
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

    game(LEVEL_DICT)


# Game Loop ------------------------------------------------------- #
def game(LEVEL_DICT, level=1):
    print(level)

    if level in LEVEL_DICT:
        drone = LEVEL_DICT[level][0]
        obstacles = LEVEL_DICT[level][1]
    else:
        return None #end game loop

    run = True
    while run:
        main_clock.tick(FPS)
            
        # Events n stuff
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: # event has no key attribute
                if event.key == pygame.K_ESCAPE:
                    run = False
                    stop_music(fadeout=True)

        if not run:
            break

        intersection_pt = check_intersection(obstacles, drone)
        alive = update_interaction(intersection_pt, drone)
            
        # Do Stuff 
        drone.move()
        for obstacle in obstacles:
            obstacle.move()

        # Update window
        update_window(drone, obstacles, intersection_pt)

        # Alive?
        if not alive:
            level += 1
            run = False
            stop_music(fadeout=True)
            

    if not alive:
        #interlevel loop
        game(LEVEL_DICT, level)
        
        

    
while True:
    menu()

# Close Pygame ------------------------------------------------ #
pygame.quit()
sys.exit()

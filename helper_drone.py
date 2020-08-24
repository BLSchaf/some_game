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

TITLE_IMG = pygame.image.load(r'assets\title_green.png').convert()
MENU_IMG = pygame.image.load(r'assets\menu.png').convert()
CAMPAIGN_IMG = pygame.image.load('assets\campaign.png').convert()
LEVEL_CURSOR_ACTIVE_IMG = pygame.image.load('assets\level_active.png').convert()
LEVEL_CURSOR_INACTIVE_IMG = pygame.image.load('assets\level_inactive.png').convert()

START_BUTTON = pygame.image.load(os.path.join('assets', 'start_button.png')).convert()
START_BUTTON_ACTIVE = pygame.image.load(os.path.join('assets', 'start_button_active.png')).convert()
QUIT_BUTTON = pygame.image.load(os.path.join('assets', 'quit_button.png')).convert()
QUIT_BUTTON_ACTIVE = pygame.image.load(os.path.join('assets', 'quit_button_active.png')).convert()
CAMPAIGN_BUTTON = pygame.image.load(os.path.join('assets', 'campaign_button.png')).convert()
CAMPAIGN_BUTTON_ACTIVE = pygame.image.load(os.path.join('assets', 'campaign_button_active.png')).convert()


#MENU_FONT = pygame.font.SysFont('Matura MT Script Capitals', 60, 1)
#MENU_LABEL = MENU_FONT.render('Helper Drone v1', False, (20, 20, 20))


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



class Button():
    def __init__(self, window, x, y, img_active, img_inactive, action, level_list=None):
        self.window = window
        self.x = x
        self.y = y
        self.width = img_active.get_width()
        self.height = img_active.get_height()
        self.img_active = img_active
        self.img_inactive = img_inactive
        self.action = action
        self.args = level_list

    def check_status(self):
        mouse = pygame.mouse.get_pos()
        
        if self.x <= mouse[0] <= self.x + self.width\
           and self.y <= mouse[1] <= self.y + self.height:
            self.img_active.set_colorkey((255,255,255))
            self.window.blit(self.img_active, (self.x, self.y))
            
            if pygame.mouse.get_pressed()[0] == 1:
                if self.args:
                    self.action(self.args)
                else:
                    self.action()
                return False
                    
        else:
            self.img_inactive.set_colorkey((255,255,255))
            self.window.blit(self.img_inactive, (self.x, self.y))

        return True


def close_all():
    pygame.quit()
    sys.exit()

    
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
        play_music('futuristic_sound.mp3')
        
    elif intersection_pt and not drone.not_charging:
        drone.not_charging = True
        drone.charging = False
        play_music('squeezy_charge.mp3')

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

    

# Title Screen ------------------------------------------------------- #
def title():
    print('title')
    button = Button(WINDOW,
                    (WIDTH - START_BUTTON.get_width())//2,
                    int(HEIGHT*.7),
                    START_BUTTON_ACTIVE,
                    START_BUTTON,
                    menu)

    run = True
    while run:
        WINDOW.blit(TITLE_IMG, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            
        button.check_status()
        pygame.display.update()

    

# Main Menu ------------------------------------------------------- #
def menu():
    print('menu')
    buttons = [
        Button(WINDOW,
               100,
               int(HEIGHT*.3),
               CAMPAIGN_BUTTON_ACTIVE,
               CAMPAIGN_BUTTON,
               campaign),
        Button(WINDOW,
               100,
               int(HEIGHT*.6),
               QUIT_BUTTON_ACTIVE,
               QUIT_BUTTON,
               close_all,
               )
        ]


    run = True
    while run:
        WINDOW.blit(MENU_IMG, (0,0))

        
        for button in buttons:
            button.check_status()

        pygame.display.update()

        # Events n stuff
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_all()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    #stop_music(fadeout=True)


# Level Menu ------------------------------------------------------- #
def campaign():
    print('campaign')

    buttons = [
        Button(WINDOW,
               80,
               210,
               LEVEL_CURSOR_ACTIVE_IMG,
               LEVEL_CURSOR_INACTIVE_IMG,
               level,
               1),
        Button(WINDOW,
               250,
               110,
               LEVEL_CURSOR_ACTIVE_IMG,
               LEVEL_CURSOR_INACTIVE_IMG,
               level,
               2),
        Button(WINDOW,
               330,
               270,
               LEVEL_CURSOR_ACTIVE_IMG,
               LEVEL_CURSOR_INACTIVE_IMG,
               level,
               3),
        Button(WINDOW,
               475,
               200,
               LEVEL_CURSOR_ACTIVE_IMG,
               LEVEL_CURSOR_INACTIVE_IMG,
               level,
               3)
        ]

    
    run = True
    while run:
        WINDOW.blit(CAMPAIGN_IMG, (0,0))

        for button in buttons:
            button.check_status()

        # Events n stuff
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_all()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    #stop_music(fadeout=True)

        pygame.display.update()
        

# Level Menu ------------------------------------------------------- #
def level(level):
    print('level_script')

    LEVEL_DICT = {
        1: [Drone((50, 50)),
            []
        ],
        2: [Drone((50, 50)),
            [
                Obstacle([(50,50), (40,100), (120,70), (130,50)]),
                Obstacle([(100,130), (120,160), (130,150)])
            ]
        ],
        3: [Drone((50, 50)),
            [
                Obstacle([(50,50), (40,100), (120,70), (130,50)]),
                Obstacle([(100,130), (120,160), (130,150)]),
                Obstacle([(400,230), (500,250), (520, 200), (480, 180), (430, 200)])
            ]
        ]             
    }
    
    # intro()
    game(LEVEL_DICT[level])
    # outro()
    pass


# Game Loop ------------------------------------------------------- #
def game(level_objects):
    print('game_level')

    drone = level_objects[0]
    obstacles = level_objects[1]

    run = True
    while run:
        main_clock.tick(FPS)
            
        # Events n stuff
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_all()

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
            run = False
            stop_music(fadeout=True)
            

    
while True:
    title()

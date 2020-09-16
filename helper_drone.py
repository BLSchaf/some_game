import pygame
import sys
import os
import random
import math


# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 400
CENTER = (WIDTH//2, HEIGHT//2)

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Helper Drone')

TITLE_IMG = pygame.image.load(r'assets\title_green.png').convert()
MENU_IMG = pygame.image.load(r'assets\title2.png').convert()
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

dt = 1 / FPS # to simulate one second for the formula

class Drone():
    def __init__(self, pos, life = 10):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.r = 10
        self.color = (180, 180, 200)
        self.vel = [0,0]
        self.acc = 5
        self.charging = False
        self.not_charging = False
        self.life = life
        

    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] == 1:
            self.vel[1] -= self.acc * dt
        elif keys[pygame.K_s] == 1:
            self.vel[1] += self.acc * dt
        else:
            if abs(self.vel[1]) < 0.1:
                self.vel[1] = 0
            else:
                self.vel[1] *= 0.99
                
        if keys[pygame.K_a] == 1:
            self.vel[0] -= self.acc * dt
        elif keys[pygame.K_d] == 1:
            self.vel[0] += self.acc * dt
        else:
            if abs(self.vel[0]) < 0.1:
                self.vel[0] = 0
            else:
                self.vel[0] *= 0.99

        self.vel[0] = max(min(self.vel[0], 5),-5)
        self.vel[1] = max(min(self.vel[1], 5),-5)

        self.x += self.vel[0]
        self.y += self.vel[1]
        self.pos = (self.x, self.y)

    def draw(self):
        pygame.draw.circle(WINDOW, self.color, (int(self.x), int(self.y)), self.r)

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
        self.points_int = [list(map(int, point)) for point in self.points]
        self.color = (220, 130, 80)
        self.x_vel = random.randint(-10,10)/10
        self.y_vel = random.randint(-10,10)/10

    def __len__(self):
        return len(self.points)

    def move(self):
        self.x_vel *= random.randint(90,110) / 100
        self.y_vel *= random.randint(90,110) / 100
        self.points = [(i + self.x_vel, j + self.y_vel) for i, j in self.points]
        self.points_int = [list(map(int, point)) for point in self.points]

    def draw(self):
        pygame.draw.polygon(WINDOW, self.color, self.points_int)



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
    return (x,y)


def get_intersection(line1, line2):
    if line1[0] == line2[1] or line1[1] == line2[1] or line1[0] == line2[0] or line1[1] == line2[0]:
        return None
    intersection_pt = calc_intersect(line1, line2)

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

    return list(map(int, calc_intersect(line1, line2)))


def check_intersection(obstacles, start, end):
    for obstacle in obstacles:
            for i in range(len(obstacle)):
                intersection_pt = get_intersection((obstacle.points[i],
                                                    obstacle.points[(i+1)%(len(obstacle))]),
                                                   (start, end))
                
                if intersection_pt:
                    return intersection_pt
                
    return None


def update_interaction(no_contact, drone, center):   
    if not no_contact:
        if drone.life >= 0.1:
            drone.life -= 0.1
            center.life += 0.1
            
    else:
        if drone.life <= 99.9:
            drone.life += 0.1
    
    if not no_contact and not drone.charging:
        drone.charging = True
        drone.not_charging = False
        play_music('wummern.mp3')
        
    elif no_contact and not drone.not_charging:
        drone.not_charging = True
        drone.charging = False
        play_music('idle_wummern.mp3')


def get_coord_diff(start, end):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    return dx, dy

def get_distance(start, end):
    dx, dy = get_coord_diff(start, end)
    return math.sqrt(dx**2 + dy**2)

def get_angle(start, end):
    dx, dy = get_coord_diff(start, end)
    return math.atan2(-dy,dx) #rads
##    degs = degrees(rads)




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
def update_window(drone, obstacles, center, no_contact):
    '''
    Updates the window
    drone: Drone instance
    obstacle: Line instance
    '''
    WINDOW.fill((50, 50, 50))
    
    

    intersection_pts = []
    vertex_list = []
    


    
    for i, obstacle_inner in enumerate(obstacles):
        for j in range(len(obstacle_inner)):
            flag_vertex = True
            vertex = obstacle_inner.points[j]
            vertex_list.append(vertex)
            
            for a, obstacle in enumerate(obstacles):
                for b in range(len(obstacle)):  
                    intersection_pt = get_intersection((obstacle.points[b],
                                                        obstacle.points[(b+1)%(len(obstacle))]),
                                                       (drone.pos, vertex))
                    
                    if intersection_pt:
                        intersection_pts.append(intersection_pt)
                        if flag_vertex == True:
                            flag_vertex = False
                            vertex_list.pop()
    
##    for intersection_pt in intersection_pts:
##        if intersection_pt:
##            pygame.draw.circle(WINDOW, (220, 220, 220), intersection_pt, 6, 1)
    for i, vertex in enumerate(vertex_list):
        #pygame.draw.aaline(WINDOW, (222,222,222), vertex, drone.pos)
        
        vertex_list[i] = vertex, get_angle(drone.pos, vertex)

    
    vertex_list.sort(key=lambda tup: tup[1])
    #print(vertex_list)

    triangles = []
    for i, vertex in enumerate(vertex_list):
        flag_triangle = True
        triangles.append((drone.pos, vertex_list[i][0], vertex_list[(i+1)%(len(vertex_list))][0]))
        if check_intersection(obstacles,
                              vertex_list[i][0],
                              vertex_list[(i+1)%(len(vertex_list))][0]):
            
            if flag_triangle == True:
                flag_triangle = False
                triangles.pop()

    # draw center
    pygame.draw.circle(WINDOW, (220, 220, 220), CENTER, 30, 2)
    pygame.draw.circle(WINDOW, (220, 220, 220), CENTER, int(center.life))

    pygame.draw.circle(WINDOW, (30, 80, 200), (300, 280), 50)

    # draw triangles of sight
    light_surf = pygame.Surface(SIZE)
    for triangle in triangles:
        pygame.draw.polygon(light_surf, (30,30,10), triangle)
    #test_surf.set_colorkey((0,0,0))
    WINDOW.blit(light_surf, (0, 0, WIDTH, HEIGHT), special_flags=pygame.BLEND_RGBA_ADD)
    
    # draw drone and obstacles    
    drone.draw()
    for obstacle in obstacles:
        obstacle.draw()

    # draw line of sight
    if no_contact:
        pass
        #pygame.draw.aaline(WINDOW, (220, 130, 80), drone.pos, CENTER)
        #pygame.draw.circle(WINDOW, (220, 220, 220), no_contact, 6, 1)
    else:
        pygame.draw.aaline(WINDOW, (130, 220, 80), drone.pos, CENTER)
        
    pygame.draw.rect(WINDOW, (80,80,80), (WIDTH - 122, 18, 104, 24))
    if drone.life >= 1:
        pygame.draw.rect(WINDOW, (220, 220, 220), (WIDTH - 120, 20, int(drone.life), 20)) 

# ****
##    test_surf = pygame.Surface((center.life*4, center.life*4))
##    pygame.draw.circle(test_surf,
##                       (20,20,20),
##                       (int(center.life*2), int(center.life*2)),
##                       int(center.life*2))
##    test_surf.set_colorkey((0,0,0))
    # ****

    #WINDOW.blit(test_surf, (int(CENTER[0]-center.life*2), int(CENTER[1]-center.life*2)), special_flags=pygame.BLEND_RGBA_ADD)

    #Line of Sight Field
    # fill triangles
    # lines slightly right and left to vertex
    
    

    
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
        1: [Drone((50, 50), 50),
            []
        ],
        2: [Drone((50, 50), 20),
            [
                Obstacle([(50,50), (40,100), (120,70), (130,50)]),
                Obstacle([(100,130), (120,160), (130,150)])
            ]
        ],
        3: [Drone((50, 50), 30),
            [
                Obstacle([(50,50), (40,100), (120,70), (130,50)]),
                Obstacle([(100,130), (120,160), (130,150)]),
                Obstacle([(400,230), (500,250), (520, 200), (480, 180), (430, 200)])
            ]
        ]             
    }
    
    # intro()
    if game(LEVEL_DICT[level]):
        pass
        #lose_outro
    else:
        pass
        #win_outro()
    pass


# Game Loop ------------------------------------------------------- #
def game(level_objects):
    print('game_level')

    drone = level_objects[0]
    obstacles = level_objects[1]

    run = True
    win = False
    center = Drone(CENTER, 5)
    
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
                    
                if event.key == pygame.K_SPACE:
                    pause = True
                    stop_music(fadeout=True)
                    print('pause start')
                    pygame.event.clear()
                    while pause:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    print('pause end')
                                    pause = False                        

        if not run:
            break
        
        no_contact = check_intersection(obstacles, drone.pos, CENTER)
        update_interaction(no_contact, drone, center)
       
        if drone.life < 0.1:
            run = False
            win = False

        if center.life >= 50:
            run = False
            win = True
            
        # Do Stuff
        drone.move()
        for obstacle in obstacles:
            pass
        #obstacle.move()

        # Update window
        update_window(drone, obstacles, center, no_contact)

    print('run = False')
    stop_music(fadeout=True)
    if win:
        print('win')
    else:
        print('lose')
        
    return win
            

    
while True:
    title()

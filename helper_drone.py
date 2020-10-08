import pygame
import sys
import os
import random
import math
from helper_intersection import *
from helper_classes import Drone, Obstacle, Button
import pygame.gfxdraw


# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 400
CENTER = (WIDTH//2, HEIGHT//2)

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode(SIZE)
MASK = pygame.surface.Surface(SIZE).convert_alpha()

pause_font = pygame.font.SysFont('Matura MT Script Capitals', 60, 1)
pause_label = pause_font.render('Pause', False, (33, 66, 112))


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


def close_all():
    pygame.quit()
    sys.exit()


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


            
# Intersection Stuff ---------------------------------------------- #
def update_intersection(obstacles, drone, center):
    # Line of Sight Intersection
    no_contact = False
    for obstacle in obstacles:
        for j in range(len(obstacle)):
            obstacle_line = (obstacle.points[j], obstacle.points[(j+1)%(len(obstacle))])
            intersection = get_intersection(obstacle_line, (drone.pos, center.pos))
            if intersection:
                no_contact = True
                break
                
        if no_contact:
            break
   
    if no_contact:
        if drone.life <= 99.9:
            drone.life += 0.1       
    else:
        if drone.life >= 0.1:
            pass
            #drone.life -= 0.1
            #center.life += 0.1
        
    if no_contact and drone.charging:
        drone.charging = False
        play_music('idle_wummern.mp3')
        
    elif not no_contact and not drone.charging:
        drone.charging = True
        play_music('wummern.mp3')



def update_line_of_sight(obstacles, drone):
    # Line to Vertices Intersection
    # get all vertices, although not needed - readability
    vertex_list = [obstacle.points[i] for obstacle in obstacles for i in range(len(obstacle))]
    vertex_list_valid = []
    intersection_list = []
    
    #get relevant vertices
    for i, vertex in enumerate(vertex_list):
        vertex_flag = True
        for obstacle in obstacles:
            for j in range(len(obstacle)):
                obstacle_line = (obstacle.points[j], obstacle.points[(j+1)%(len(obstacle))])
                intersection = get_intersection(obstacle_line, (drone.pos, vertex))
                
                if intersection:
                    vertex_flag = False
               
                        
        # for relevant vertices create two new rays
        if vertex_flag:
            current_angle = get_angle(drone.pos, vertex)
            vertex_list_valid.append([vertex, current_angle])
 
            radar_len = math.sqrt(WIDTH**2 + HEIGHT**2)
            angle_plus = current_angle+0.001
            angle_minus = current_angle-0.001
            if angle_plus > math.pi*2:
                angle_plus -= math.pi*2
            if angle_minus < 0:
                angle_minus += math.pi*2
            angle_change = [angle_plus, angle_minus]

            for angle in angle_change:
                x = drone.pos[0] + math.cos(angle) * radar_len
                y = drone.pos[1] - math.sin(angle) * radar_len
                
                possible_intersects = []
                for obstacle in obstacles:
                    for j in range(len(obstacle)):
                        obstacle_line = (obstacle.points[j], obstacle.points[(j+1)%(len(obstacle))])
                        intersect = get_intersection(obstacle_line, (drone.pos, (x, y)))
                        if intersect:
                            possible_intersects.append(intersect)

                            
                min_distance = radar_len
                for intersect in possible_intersects:
                    distance = get_distance(drone.pos, intersect)
                    if distance < min_distance:
                        min_distance = distance
                        closest_intersect = intersect
                        
                intersection_list.append(closest_intersect)
                vertex_list_valid.append([closest_intersect, angle])
            

    # sort all relevant vertices
    vertex_list_valid.sort(key=lambda tup: tup[1])

    # Tirangles (***no vertex when out of bounds***)
    triangles = []
    for i, vertex in enumerate(vertex_list_valid):
        vertex_line = vertex_list_valid[i][0], vertex_list_valid[(i+1)%(len(vertex_list_valid))][0]
        triangles.append((drone.pos, vertex_line[0], vertex_line[1]))

    return triangles, intersection_list



# Update Game Window ---------------------------------------------- #
def update_window(center, triangles, drone, obstacles, intersection_list):
    WINDOW.fill((180,180,180))
    MASK.fill((0,0,0,255))
    
    # draw center
    pygame.draw.circle(WINDOW, (220, 220, 220), CENTER, 30, 2)
    pygame.draw.circle(WINDOW, (220, 220, 220), CENTER, int(center.life))

    pygame.draw.circle(WINDOW, (30, 80, 200), (300, 280), 50)

##    for intersection in intersection_list:
##        pygame.draw.circle(WINDOW, (80, 20, 230), intersection, 6, 1)
##    for i, vertex in enumerate(vertex_list):
##    pygame.draw.aaline(WINDOW, (222,222,222), vertex, drone.pos)
        
    # draw triangles of sight
##    light_surf = pygame.Surface(SIZE)
##    for i, triangle in enumerate(triangles):
##        #pygame.draw.polygon(light_surf, (min(255,(i+1)*10),min(255,(i+1)*20),min(255,(i+1)*3)), triangle)
##        pygame.draw.polygon(light_surf, (10, 20, 3), triangle)
##    #test_surf.set_colorkey((0,0,0))
##    WINDOW.blit(light_surf, (0, 0, WIDTH, HEIGHT), special_flags=pygame.BLEND_RGBA_ADD)
    
    for triangle in triangles:
        pygame.gfxdraw.filled_polygon(MASK, triangle, (0, 0, 0, 0))
        #pygame.draw.polygon(MASK, (0, 0, 0, 0), triangle)

    
    # draw drone and obstacles    
    drone.draw(WINDOW)
   
        
     

    
    WINDOW.blit(MASK,(0,0))
    
    for obstacle in obstacles:
        obstacle.draw(WINDOW)

    pygame.draw.rect(WINDOW, (80,80,80), (WIDTH - 122, 18, 104, 24))
    if drone.life >= 1:
        pygame.draw.rect(WINDOW, (220, 220, 220), (WIDTH - 120, 20, int(drone.life), 20))
    
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
        

# Level Orchestrator ------------------------------------------------------- #
def level(level):
    print('level_script')
    borders = Obstacle([(-1,0), (WIDTH, 0), (WIDTH+1, HEIGHT), (0, HEIGHT)], (0,0), False)
    LEVEL_DICT = {
        1: [Drone((200, 200), 50),
            [
                borders
            ]
        ],
        2: [Drone((200, 200), 20),
            [
                borders,
                Obstacle([(10,10), (0,60), (80,30), (90,10)], (200,200)),
                Obstacle([(0,30), (20,60), (30,50)], (450,150))
            ]
        ],
##        3: [Drone((200,200), 30),
##            [
##                borders,
##                Obstacle([(50,50), (40,100), (120,70), (130,50)]),
##                Obstacle([(100,130), (120,160), (130,150)]),
##                Obstacle([(400,230), (500,250), (520, 200), (480, 180), (430, 200)]),
##                Obstacle([(250, 280), (261,290), (260, 300), (250, 310), (241, 300), (240, 290)]),
##                Obstacle([(50, 300), (120, 380), (30, 280), (40, 290)]),
##                Obstacle([(350, 180), (400, 180), (401, 140), (351, 140)])
##            ]
##        ]             
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
                        WINDOW.blit(
                            pause_label,
                            (
                                (WIDTH - pause_label.get_width())//2,
                                round(HEIGHT*.33 + pause_label.get_height() + 10)
                            )
                        )
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    print('pause end')
                                    pause = False                        

        if not run:
            break
        
        
        #calc all intersections and polygons and stuff
        triangles, intersection_list = update_line_of_sight(obstacles, drone)
        update_intersection(obstacles, drone, center)
       
        # Do Stuff
        if drone.life < 0.1:
            run = False
            win = False

        if center.life >= 50:
            run = False
            win = True

        for i, obstacle in enumerate(obstacles):
            
            drone.repel(obstacle.collision(drone), obstacle)
            obstacle.move()
            
            for other_obstacle in obstacles[i+1:]:
                obstacle.collision(other_obstacle)


        drone.move(FPS)
        if drone.x <= 0:
            drone.x = 1
            drone.vel[0] = 0
        if drone.x >= WIDTH:
            drone.x = WIDTH-1
            drone.vel[0] = 0
        if drone.y <= 0:
            drone.y = 1
            drone.vel[1] = 0
        if drone.y >= HEIGHT:
            drone.y = HEIGHT -1
            drone.vel[1] = 0
        drone.update_pos()
        
        # Update window
        # draw line of sight
##        if no_contact:
##            pass
##            #pygame.draw.aaline(WINDOW, (220, 130, 80), drone.pos, CENTER)
##            #pygame.draw.circle(WINDOW, (220, 220, 220), no_contact, 6, 1)
##        else:
##            pygame.draw.aaline(WINDOW, (130, 220, 80), drone.pos, CENTER)
            
        update_window(center, triangles, drone, obstacles, intersection_list)

    print('run = False')
    stop_music(fadeout=True)
    if win:
        print('win')
    else:
        print('lose')
        
    return win
            

    
while True:
    title()

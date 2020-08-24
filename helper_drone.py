import pygame, sys, os, random


# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 400
CENTER = (WIDTH//2, HEIGHT//2)

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Helper Drone')

<<<<<<< Updated upstream
<<<<<<< Updated upstream
TITLE_IMG = pygame.image.load('assets\HD_title.png')
PLAY_BUTTON_UP = pygame.image.load(os.path.join('assets', 'HD_title_play_up.png')).convert()
PLAY_BUTTON_DOWN = pygame.image.load(os.path.join('assets', 'HD_title_play_down.png')).convert()
=======
TITLE_IMG = pygame.image.load(os.path.join('assets', 'title2.png')).convert()
MENU_IMG = pygame.image.load(os.path.join('assets', 'menu.png')).convert()

=======
TITLE_IMG = pygame.image.load(r'assets\title_green.png').convert()
MENU_IMG = pygame.image.load(r'assets\menu.png').convert()
>>>>>>> Stashed changes
CAMPAIGN_IMG = pygame.image.load('assets\campaign.png').convert()
LEVEL_CURSOR_ACTIVE_IMG = pygame.image.load('assets\level_active.png').convert()
LEVEL_CURSOR_INACTIVE_IMG = pygame.image.load('assets\level_inactive.png').convert()
PLAY_BUTTON_UP = pygame.image.load(os.path.join('assets', 'start_blau.png')).convert()
PLAY_BUTTON_DOWN = pygame.image.load(os.path.join('assets', 'start_rot.png')).convert()

QUIT_BUTTON_UP = pygame.image.load(os.path.join('assets', 'quit_blau.png')).convert()
QUIT_BUTTON_DOWN = pygame.image.load(os.path.join('assets', 'quit_rot.png')).convert()
>>>>>>> Stashed changes

CAMPAIGN_BUTTON_UP = pygame.image.load(os.path.join('assets', 'campaign_blau.png')).convert()
CAMPAIGN_BUTTON_DOWN = pygame.image.load(os.path.join('assets', 'campaign_rot.png')).convert()

#MENU_FONT = pygame.font.SysFont('Matura MT Script Capitals', 60, 1)
#MENU_LABEL = MENU_FONT.render('Helper Drone v1', False, (20, 20, 20))



class Drone():
    def __init__(self, pos, life = 100):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.r = 10
        self.color = (220, 220, 220)
        self.vel = 3
        self.charging = False
        self.not_charging = False
<<<<<<< Updated upstream
=======
        self.life = life
        
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
        self.color = (200, 130, 70)

    def draw(self):
        pygame.draw.aalines(WINDOW, self.color, True, self.points)

=======
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
>>>>>>> Stashed changes


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


<<<<<<< Updated upstream
=======
def check_intersection(obstacles, drone):
    for obstacle in obstacles:
            for i in range(len(obstacle)):
                intersection_pt = get_intersection((obstacle.points[i],
                                                    obstacle.points[(i+1)%(len(obstacle))]),
                                                   (drone.pos, CENTER))
                
                if intersection_pt:
                    return intersection_pt
                
    return None


def update_interaction(intersection_pt, drone, center):
    drone.color = (min(2.5* drone.life, 255)/2, 0, min(0.5* drone.life, 255)/2)
    if not intersection_pt:
        if drone.life >= 0.1:
            drone.life -= 0.1
            center.life += 0.1
            
    else:
        if drone.life <= 99.9:
            drone.life += 0.1
    
    if not intersection_pt and not drone.charging:
        drone.charging = True
        drone.not_charging = False
        play_music('wummern.ogg')
        
    elif intersection_pt and not drone.not_charging:
        drone.not_charging = True
        drone.charging = False
        play_music('idle_wummern.ogg')
        



>>>>>>> Stashed changes


def play_music(music, pos=0, vol=0.05):
    pygame.mixer.music.set_volume(vol)
    #pygame.mixer.music.set_pos(pos)
    pygame.mixer.music.load(f'assets\{music}')
    pygame.mixer.music.play(-1, pos)

def stop_music(stop=False):
    if stop:
        pygame.mixer.music.stop()
    pygame.mixer.music.fadeout(300)
    
    

# Update Game Window ---------------------------------------------- #
<<<<<<< Updated upstream
def update_window(drone, obstacle):
=======
def update_window(drone, obstacles, intersection_pt, center):
>>>>>>> Stashed changes
    '''
    Updates the window
    drone: Drone instance
    obstacle: Line instance
    '''
    WINDOW.fill((50, 50, 50))
    
<<<<<<< Updated upstream
    pygame.draw.circle(WINDOW, (220, 220, 220), CENTER, 30)
=======
    pygame.draw.circle(WINDOW, (220, 220, 220), CENTER, 30, 5)
    pygame.draw.circle(WINDOW, (0, min(8.5 * center.life, 255), 0), CENTER, int(center.life))

    #drone life
    pygame.draw.rect(WINDOW, (80,80,80), (WIDTH - 122, 18, 104, 24))
    pygame.draw.rect(WINDOW, (220, 220, 220), (WIDTH - 120, 20, int(drone.life), 20))
    
>>>>>>> Stashed changes
    drone.draw()
    obstacle.draw()

    intersection_pt = segment_intersect((obstacle.points[0], obstacle.points[1]), (drone.pos, CENTER))

    if intersection_pt:
        pygame.draw.line(WINDOW, (220, 130, 80), drone.pos, CENTER)
        pygame.draw.circle(WINDOW, (220, 220, 220), intersection_pt, 6, 1)
    else:
        pygame.draw.line(WINDOW, (130, 220, 80), drone.pos, CENTER)
    
    pygame.display.update()

<<<<<<< Updated upstream
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
=======
    

# Title Screen ------------------------------------------------------- #
def title():
    print('title')
    button = Button(WINDOW,
                    (WIDTH - PLAY_BUTTON_UP.get_width())//2,
                    int(HEIGHT*.7),
                    PLAY_BUTTON_DOWN,
                    PLAY_BUTTON_UP,
                    menu)

    run = True
    while run:
        WINDOW.blit(TITLE_IMG, (0,0))
        #WINDOW.blit(MENU_LABEL, (100, int(HEIGHT*.1)))
        
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
               CAMPAIGN_BUTTON_DOWN,
               CAMPAIGN_BUTTON_UP,
               campaign),
        Button(WINDOW,
               100,
               int(HEIGHT*.6),
               QUIT_BUTTON_DOWN,
               QUIT_BUTTON_UP,
               close_all,
               )
        ]


    run = True
    while run:
        WINDOW.blit(MENU_IMG, (0,0))
        #WINDOW.blit(MENU_LABEL, (100, int(HEIGHT*.1)))

>>>>>>> Stashed changes
        
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

<<<<<<< Updated upstream
    game()


# Game Loop ------------------------------------------------------- #
def game():
    drone = Drone((50, 50))
<<<<<<< Updated upstream
    obstacle = Line((random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                    (random.randint(0, WIDTH), random.randint(0, HEIGHT)))
=======
    obstacle = Obstacle([(100, 50), (40, 60), (320, 200)])
>>>>>>> Stashed changes
=======
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
    win = game(LEVEL_DICT[level])
    if win:
        # win outro()
        pass
    else:
        # lose outro()
        pass
    pass


# Game Loop ------------------------------------------------------- #
def game(level_objects):
    print('game_level')

    drone = level_objects[0]
    obstacles = level_objects[1]
    center = Drone(CENTER, 5)
>>>>>>> Stashed changes

    
    
    run = True
    win = False
    
    while run:
        
        intersection_pt = segment_intersect((obstacle.points[0], obstacle.points[1]), (drone.pos, CENTER))
        if not intersection_pt and not drone.charging:
            drone.charging = True
            drone.not_charging = False
            play_music('wummern.mp3')
        elif intersection_pt and not drone.not_charging:
            stop_music(stop=True)
            drone.charging = False
            drone.not_charging = True
            play_music('idle_wummern.mp3')
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
            
        # Buttons n stuff
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: # event has no key attribute
                if event.key == pygame.K_ESCAPE:
                    run = False

<<<<<<< Updated upstream
=======
        intersection_pt = check_intersection(obstacles, drone)
        update_interaction(intersection_pt, drone, center)
        print(drone.life, center.life, drone.color)
        
        if drone.life <= 0.1:
            run = False
            win = False

        if center.life >= 30:
            run = False
            win = True

>>>>>>> Stashed changes
        # Do Stuff 
        drone.move()

        # Update window
<<<<<<< Updated upstream
        update_window(drone, obstacle)
        main_clock.tick(FPS)
=======
        update_window(drone, obstacles, intersection_pt, center)

    stop_music(fadeout=True)
    if win:
        print('win')
            
>>>>>>> Stashed changes

    
while True:
    menu()

# Close Pygame ------------------------------------------------ #
pygame.quit()
sys.exit()

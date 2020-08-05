import pygame
import sys, random
import os

# import random

# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 400
CENTER = ((WIDTH//2, HEIGHT//2))

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((SIZE))
pygame.display.set_caption('Helper Drone')


TITLE_IMG = pygame.image.load(os.path.join('assets', 'Title.png'))
TITLE2_IMG = pygame.image.load(os.path.join('assets', 'Title2.png'))
TITLE2GOLD_IMG = pygame.image.load(os.path.join('assets', 'Title2_gold.png'))


menu_font = pygame.font.SysFont('Matura MT Script Capitals', 60, 1)
menu_label = menu_font.render('Some Menu Title', False, (0,0,0))
WINDOW.blit(menu_label, (130, round(HEIGHT*.33)))

class Drone():
    def __init__(self, pos):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.r = 10
        self.color = (180, 180, 150)
        self.vel = 9
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

    def set_inbound(self):
        # Boundaries
        if self.x < 0:#links
            self.x = 0 + self.r
        if self.x + self.r > self.WIDTH:#rechts
            self.x = self.WIDTH - self.r
        if self.y < 0: #oben
            self.y = 0 + self.r
        if self.y + self.r > self.HEIGHT: #unten
            self.y = self.HEIGHT - self.r

    def move(self):
        keys = pygame.key.get_pressed()
        key = pygame.key.get_pressed()
        if key[pygame.K_w] or key[pygame.K_UP]: # move up
            self.y -= self.vel
        if key[pygame.K_s] or key[pygame.K_DOWN]: # move down
            self.y += self.vel
        if key[pygame.K_a] or key[pygame.K_LEFT]: # move left
            self.x -= self.vel
        if key[pygame.K_d] or key[pygame.K_RIGHT]: # move right
            self.x += self.vel

        self.pos = (self.x, self.y)

        self.set_inbound()

    def draw(self):
        pygame.draw.circle(WINDOW, self.color, (self.x, self.y), self.r, 1)


class Line():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.color = (220, 100, 70)

    def draw(self):
        pygame.draw.line(WINDOW, self.color, self.start, self.end)


def slope(p1, p2):
    print(p1, p2)
    return (p2[1] - p1[1]) * 1./ (p2[0] - p1[0])
   
def y_intercept(slope, p1) :
    return p1[1] - 1.* slope * p1[0] # y = mx+b -> b = y-mb | b:= y_intercept

def intersect(line1, line2) :
    min_allowed = 1e-5   # guard against overflow
    big_value = 1e10     # use instead (if overflow would have occurred)
    m1 = slope(line1[0], line1[1])
    b1 = y_intercept(m1, line1[0])

    m2 = slope(line2[0], line2[1])
    b2 = y_intercept(m2, line2[0])

    if abs(m1 - m2) < min_allowed:
        x = big_value
    else :
        x = (b2 - b1) / (m1 - m2)
      
    y = m1 * x + b1
    #y2 = m2 * x + b2
    return (int(x),int(y))

def segment_intersect(line1, line2):
    intersection_pt = intersect(line1, line2)

    if(line1[0][0] < line1[1][0]):
        if intersection_pt[0] < line1[0][0] or intersection_pt[0] > line1[1][0]:
            return None
    else:
        if intersection_pt[0] > line1[0][0] or intersection_pt[0] < line1[1][0]:
            return None
         
    if(line2[0][0] < line2[1][0]):
        if intersection_pt[0] < line2[0][0] or intersection_pt[0] > line2[1][0]:
            return None
    else:
        if intersection_pt[0] > line2[0][0] or intersection_pt[0] < line2[1][0]:
            return None

    return intersection_pt
        


        
def update_window(drone, obstacle):
    WINDOW.fill((50,0,0))
    pygame.draw.circle(WINDOW, (200, 200, 200), (CENTER), 30)
    drone.draw()
    obstacle.draw()
    
    intersection_pt = segment_intersect((obstacle.start, obstacle.end), (drone.pos, CENTER))

    if intersection_pt:
        pygame.draw.line(WINDOW, (220, 130, 80), drone.pos, CENTER)
        pygame.draw.circle(WINDOW, (220, 220, 220), intersection_pt, 6, 1)
    else:
        pygame.draw.line(WINDOW, (130, 220, 80), drone.pos, CENTER)

        
    pygame.display.update()



def menu():
    WINDOW.blit(TITLE_IMG, (0,0))
    pygame.display.update()
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                
        pos = pygame.mouse.get_pos()
        if 112 <= pos[0] <= 355 and 258 <=pos [1] <=376:
            WINDOW.blit(TITLE2_IMG, (0,0))
            pygame.display.update()
            play_sound()
        else:
            pygame.mixer.music.fadeout(1000)
            WINDOW.blit(TITLE_IMG, (0,0))
            pygame.display.update()
            

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 112 <= pos[0] <= 355 and 258 <= pos[1] <=376:
                if event.button == 1:
                    pygame.mixer.music.fadeout(1000)
                    main()
            
        
def play_sound():
    pygame.mixer.music.load('assets\schiffshorn.mp3')
    pygame.mixer.music.set_volume(0.02)
    pygame.mixer.music.play()

                

# Loop -------------------------------------------------------- #
def main():
    drone = Drone((50, 50))
    obstacle = Line((random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                    (random.randint(0, WIDTH), random.randint(0, HEIGHT)))


    while True:
       

        # Buttons n stuff ----------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            pass

        drone.move()
        update_window(drone, obstacle)
        
        # Update window ------------------------------------------- #
        pygame.display.update()
        main_clock.tick(FPS)

menu()       
        
# Close Pygame ------------------------------------------------ #
pygame.quit()
sys.exit()

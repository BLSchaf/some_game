import pygame
import random


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
        self.life = life
        
    def move(self, fps):
        dt = 1 / fps  # to simulate one second for the formula
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

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.r)

    def is_in_sight(self):
        pass



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

    def draw(self, window):
        pygame.draw.polygon(window, self.color, self.points_int)



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



"""
class Line():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.color = (220, 130, 80)

    def draw(self, window):
        pygame.draw.line(window, self.color, self.start, self.end)

"""

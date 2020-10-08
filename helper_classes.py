import pygame
import random


class Drone():
    def __init__(self, pos, life = 10):

        ORIGINAL_SIZE = 20,20
        ORIGINAL_SURFACE = pygame.Surface(ORIGINAL_SIZE, pygame.SRCALPHA)
        self.original_surface = ORIGINAL_SURFACE
        self.surface_rect = self.original_surface.get_rect(center=pos)
        
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.r = 10
        self.color = (220, 80, 30)
        self.vel = [0,0]
        self.acc = 5
        self.charging = False
        self.life = life
        pygame.draw.circle(ORIGINAL_SURFACE, self.color, (10,10), self.r)
        self.mask = pygame.mask.from_surface(self.original_surface)
        
        
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

    def update_pos(self):
         self.pos = (self.x, self.y)
         self.surface_rect.center = self.pos

    def draw(self, window):
        window.blit(self.original_surface, self.surface_rect)

    def repel(self, collision, obstacle):
        if collision:
            if abs(self.vel[0]) > abs(obstacle.vel[0]):
                self.vel[0] *= -1.4
            elif abs(self.vel[0]) < abs(obstacle.vel[0]):
                self.vel[0] = obstacle.vel[0] * 1.4
                
                
            if abs(self.vel[1]) > abs(obstacle.vel[1]):
                self.vel[1] *= -1.4
            elif abs(self.vel[1]) < abs(obstacle.vel[1]):
                self.vel[1] = obstacle.vel[1] * 1.4
            



class Obstacle():
    def __init__(self, points, center, visible=True):
        
        ORIGINAL_SIZE = 200, 200
        ORIGINAL_SURFACE = pygame.Surface(ORIGINAL_SIZE, pygame.SRCALPHA)
        self.offset = ORIGINAL_SIZE[0]//2   
        self.center = center
        self.points = [(i + center[0], j + center[1]) for i, j in points]
        self.points_int = [list(map(int, point)) for point in points]
        
        self.visible = visible
        if self.visible:
            self.color = (220, 130, 80)
            self.points = [(i + center[0]-self.offset, j + center[1]-self.offset) for i, j in points]
            self.points_int = [list(map(int, point)) for point in points]
            pygame.draw.polygon(ORIGINAL_SURFACE, self.color, self.points_int)

            # needed for later rotation (rotate from original)
            self.original_surface = ORIGINAL_SURFACE
            self.surface_rect = self.original_surface.get_rect(center=self.center)
            self.mask = pygame.mask.from_surface(self.original_surface)

            self.vel = pygame.math.Vector2(random.randint(-10,10)/10, random.randint(-10,10)/10)

    def __len__(self):
        return len(self.points)

    def move(self):
        if self.visible:
            #self.vel *= random.randint(90,110) / 100
            self.center += self.vel
            self.surface_rect.center = self.center

            # points are offset by surface center
            self.points = [(i + self.vel[0], j + self.vel[1]) for i, j in self.points]
            self.points_int = [list(map(int, point)) for point in self.points]
    

    def draw(self, window):
        if self.visible:
            window.blit(self.original_surface, self.surface_rect)

    def collision(self, obj):
        if self.visible:
            offset = self.surface_rect[0] - obj.surface_rect[0],self.surface_rect[1] - obj.surface_rect[1]
            overlap = obj.mask.overlap(self.mask, offset)

            if overlap:
                return True
        


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

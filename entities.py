import pygame
import random
import settings as s
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import glob


# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, size=s.PLAYER_SIZE, color=s.ORANGE):
        super(Player, self).__init__()
        self.surf = pygame.image.load("assets/images/car.png")
        self.surf = pygame.transform.scale(self.surf, size)
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.size = size
        self.s_x = (s.WINDOW_WIDTH-size[0])/2
        self.s_y = 0.0
        self.v_x = 0.0
        self.v_y = 0.0
        self.C_x = 0.99
        self.C_y = 0.999
        self.C_f = 0.9
        self.C_r = 0.2
        self.crash = 0.5
        self.left_border = 0
        self.right_border = s.WINDOW_WIDTH
        # self.rect.center = window.get_rect().center
        self.rect.bottom = s.WINDOW_HEIGHT-50
        
        self.max_speed = 0.0

    def update(self, u_x=0, u_y=0):
        
        u_x = max(-1, min(u_x, 1))
        u_y = max(-1, min(u_y, 1))
        
        a_x = u_x * 0.5
        a_y = u_y * 0.1
        
        self.v_x = self.C_x * self.v_x + a_x
        self.v_y = self.C_y * self.v_y + a_y 

        # Keep player on the screen
        if self.s_x < self.left_border:
            self.s_x = self.left_border
            self.v_x =  -self.C_r*self.v_x
            self.v_y = self.C_f*self.v_y
        elif self.s_x > self.right_border - self.size[0]:
            self.s_x = self.right_border - self.size[0]
            self.v_x =  -self.C_r*self.v_x
            self.v_y = self.C_f*self.v_y
        
        # Static friction 
        tres = 1e-3
        if abs(self.v_x)<tres:
            self.v_x = 0
        if abs(self.v_y)<tres:
            self.v_y = 0

        self.s_x += self.v_x
        self.s_y += self.v_y
        self.rect.left = self.s_x
        
        if self.v_y > self.max_speed:
            self.max_speed = self.v_y
        
        if s.DEBUG:
            print(f"player velocity: {(self.v_x, self.v_y)}")
            print(f"player distance: {self.s_y}")

    
    def penalize(self):
        self.v_y = self.v_y * self.crash
            

# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, s_x, s_y, size=s.ENEMY_SIZE, color=(0,0,0)):
        super(Enemy, self).__init__()
        images = glob.glob("assets/images/enemies/*")
        self.random_image = random.choice(images)
        self.surf = pygame.image.load(self.random_image)
        self.surf = pygame.transform.scale(self.surf, size)
        self.rect = self.surf.get_rect()
        self.bottom_border = s.WINDOW_HEIGHT
        # self.surf.set_colorkey((255, 0, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        
        self.rect.left = s_x
        self.s_y = s_y
        

    def update(self, s_y):
        
        self.rect.bottom = self.bottom_border - 50 - (self.s_y - s_y)

        if self.rect.bottom > self.bottom_border + 1000:
            self.kill()


# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class RoadMarker(pygame.sprite.Sprite):
    def __init__(self, s_x, s_y, size=(10,70), color=(0, 0, 0)):
        super(RoadMarker, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.surf.set_alpha(50)
        self.rect = self.surf.get_rect()
        self.bottom_border = s.WINDOW_HEIGHT
        # self.surf.set_colorkey((255, 0, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed

        self.rect.left = s_x
        self.s_y = s_y

    def update(self, s_y):
        self.rect.bottom = self.bottom_border - 50 - (self.s_y - s_y)

        if self.rect.bottom > self.bottom_border + 1000:
            self.kill()


class Finish(pygame.sprite.Sprite):
    def __init__(self, s_x=0, s_y=s.TRACK_LENGTH, size=(s.WINDOW_WIDTH,50), color=(0, 0, 0)):
        super(Finish, self).__init__()
        self.surf = pygame.image.load("assets/images/finish.jpeg")
        #self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.bottom_border = s.WINDOW_HEIGHT
        # self.surf.set_colorkey((255, 0, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed

        self.rect.left = s_x
        self.s_y = s_y

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self, s_y):
        self.rect.bottom = self.bottom_border - 50 - (self.s_y - s_y)
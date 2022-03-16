import pygame
import random
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


# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, window, size=(40, 60), color=(255,255,255)):
        super(Player, self).__init__()
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.size = size
        self.s_x = (window.get_rect().right-size[0])/2
        self.s_y = 0.0
        self.v_x = 0.0
        self.v_y = 0.0
        self.C_x = 0.99
        self.C_y = 0.999
        self.C_b = 0.9
        self.bounce = 0.1
        self.penalty = 0.5
        self.left_border = 0
        self.right_border = window.get_rect().right
        # self.rect.center = window.get_rect().center
        self.rect.bottom = window.get_rect().bottom-50


    # Move the sprite based on keypresses
    def update(self, u_x=0, u_y=0):
        
        u_x = max(-1, min(u_x, 1))
        u_y = max(-1, min(u_y, 1))
        
        a_x = u_x * 1
        a_y = u_y * 0.05
        
        self.v_x = self.C_x * self.v_x + a_x
        self.v_y = self.C_y * self.v_y + a_y 

        # Keep player on the screen
        if self.s_x < self.left_border:
            self.s_x = self.left_border
            self.v_x =  -self.bounce*self.v_x
            self.v_y = self.C_b*self.v_y
        elif self.s_x > self.right_border - self.size[0]:
            self.s_x = self.right_border - self.size[0]
            self.v_x =  -self.bounce*self.v_x
            self.v_y = self.C_b*self.v_y
            
        tres = 1e-3
        if abs(self.v_x)<tres:
            self.v_x = 0
        if abs(self.v_y)<tres:
            self.v_y = 0

        self.s_x += self.v_x
        self.s_y += self.v_y
        self.rect.left = self.s_x
        
        print((self.v_x, self.v_y))
        print((self.s_y))
        # print((self.rect.left))
    
    def penalize(self):
        self.v_y = self.v_y * self.penalty
            

# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, window):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((40, 40))
        self.bottom = window.get_rect().bottom
        # self.surf.set_colorkey((255, 0, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(window.get_rect().left + 20, window.get_rect().right - 20),
                window.get_rect().top-100,
            )
        )

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self, v_y):
        self.rect.move_ip(0, v_y)
        if self.rect.bottom > self.bottom:
            self.kill()


# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class RoadMarker(pygame.sprite.Sprite):
    def __init__(self, window):
        super(RoadMarker, self).__init__()
        self.surf = pygame.Surface((20, 10))
        # self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                400,
                0
            )
        )
        
    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
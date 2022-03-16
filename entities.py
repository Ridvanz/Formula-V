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
    def __init__(self, window):
        super(Player, self).__init__()
        self.surf = pygame.Surface((40, 60))
        self.surf.fill((100,100,0))
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        
        self.distance = 0
        self.v_x = 0.0
        self.v_y = 0.0
        self.C_d = 0.99
        self.C_b = 0.8
        self.bounce = 0.1
        self.penalty = 0.5
        self.left_border = 0
        self.right_border = window.get_rect().right
        self.rect.bottom = window.get_rect().bottom-50
        self.rect.center = window.get_rect().center

    # Move the sprite based on keypresses
    def update(self, u_x=0, u_y=0):
        
        u_x = max(-1, min(u_x, 1))
        u_y = max(-1, min(u_y, 1))
        
        a_x = u_x * 1
        a_y = u_y * 1
        
        self.v_x = self.C_d * self.v_x + a_x
        self.v_y = self.C_d * self.v_y + a_y 
        # 
        
        if abs(self.v_x)<0.001:
            self.v_x = 0
        if abs(self.v_y)<0.001:
            self.v_y = 0
    

        self.rect.move_ip(self.v_x, 0)
        self.distance += self.v_y

        print((self.v_x, self.v_y))
        print((self.distance))
        

        # Keep player on the screen
        if self.rect.left < self.left_border:
            self.rect.left = self.left_border
            self.v_x =  -self.bounce*self.v_x
            self.v_y = self.C_b*self.v_y
        elif self.rect.right > self.right_border:
            self.rect.right = self.right_border
            self.v_x =  -self.bounce*self.v_x
            self.v_y = self.C_b*self.v_y
    
    def penalize(self):
        self.v_y = self.v_y * self.penalty
            
        


# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.set_colorkey((255, 0, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
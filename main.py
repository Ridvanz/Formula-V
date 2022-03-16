# Import the pygame module
import pygame
import time
import random
import math
from entities import Player, Enemy, RoadMarker
# import numpy as np

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)

pygame.display.set_caption("Formula V")

# Define constants for the screen width and height
FPS = 60
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800


# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
window = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))


# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 200)
ADDCLOUD = pygame.USEREVENT + 2
# pygame.time.set_timer(ADDCLOUD, 1000)
pygame.event.set_blocked ( pygame.MOUSEMOTION )

# Create our 'player'
player = Player(window)

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
# pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
# pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
# move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
# move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
# collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set the base volume for all sounds
# move_up_sound.set_volume(0.5)
# move_down_sound.set_volume(0.5)
# collision_sound.set_volume(0.5)
# Variable to keep our main loop running
running = True
tick = 0
distance = 0
# Our main loop
while running:
    
# EVENT HANDLING ############################################################
    
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy(window)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Should we add a new cloud?
        # elif event.type == ADDCLOUD:
        #     # Create the new cloud, and add it to our sprite groups
        #     new_cloud = Cloud()
        #     clouds.add(new_cloud)
        #     all_sprites.add(new_cloud)

    # Get the set of keys pressed and check for user input

#LOGIC UPDATE  ############################################################
    u_x = u_y = 0
    
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys:
        if pressed_keys[K_UP]:
            u_y = 1
            # move_up_sound.play()
        if pressed_keys[K_DOWN]:
            u_y = -1
            # move_down_sound.play()
        if pressed_keys[K_LEFT]:
            u_x = -1
        if pressed_keys[K_RIGHT]:
            u_x = 1
    
    # u_x, u_y = controller(gy)
    
    player.update(u_x, u_y)
    
    # Update the position of our enemies and clouds
    enemies.update(player.v_y)
    # clouds.update(player.v_y)

#RENDERING ############################################################
    # Fill the screen with sky blue
    red = max(0,min(255,player.v_y*5))
    window.fill((red, 250, 255-red))
    

    # Draw all our sprites
    for entity in all_sprites:
        window.blit(entity.surf, entity.rect)
    
    collided = pygame.sprite.spritecollideany(player, enemies)
    # Check if any enemies have collided with the player
    if collided:
        # If so, remove the player
        player.penalize()
        
        collided.kill()

        # Stop any moving sounds and play the collision sound
        # move_up_sound.stop()
        # move_down_sound.stop()
        # collision_sound.play()

        # Stop the loop
        # running = False

    screen.fill((0, 0, 0))
    screen.blit(window, ((SCREEN_WIDTH-WINDOW_WIDTH)/2, (SCREEN_HEIGHT-WINDOW_HEIGHT)/2))
    
    
    # pygame.draw.rect(window, RED, (0, 800, 0, 100))
    # Flip everything to the display
    pygame.display.update()

# END ############################################################
    tick += 1
    # Ensure we maintain a 30 frames per second rate
    clock.tick(FPS)
############################################################
    

print(f"reached the finish in {tick} ticks!")
# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()

#%%


# Import the pygame module
import pygame
import time
import random
import math
from entities import Player, Enemy, RoadMarker
import settings as s
from utils import try_quit


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



pygame.display.set_caption("Formula V")

# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant s.SCREEN_WIDTH and s.SCREEN_HEIGHT
screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
window = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_HEIGHT))

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 200)
ADDCLOUD = pygame.USEREVENT + 2
# pygame.time.set_timer(ADDCLOUD, 1000)
pygame.event.set_blocked ( pygame.MOUSEMOTION )

# Create our 'player'
player = Player()

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

# generate y coordinates for obstacles on the course #######################

obstacles_y = [0]
for i in range(s.NUM_OBSTACLES-1):
    randint = random.randint(100,200)
    obstacles_y.append(obstacles_y[i] + randint)

obstacles_y = [x/obstacles_y[-1]*(s.TRACK_LENGTH-s.SPAWN_AREA)+s.SPAWN_AREA for x in obstacles_y][:-1]
obstacles_x = [random.randint(0.5*s.ENEMY_SIZE[0], s.WINDOW_WIDTH - 1.5*s.ENEMY_SIZE[0]) for x in range(len(obstacles_y))]

###############################################################

# for obs_loc in obstacle_locs:
#     new_enemy = Enemy(window, s_y = obs_loc - player.s_y)
#     enemies.add(new_enemy)
#     all_sprites.add(new_enemy)


running = True
tick = 0
obs_index = 0
crashes = 0
# Our main loop
while running:
    
# EVENT HANDLING ############################################################
    
    # Look at every event in the queue
    for event in pygame.event.get():
        try_quit(event)

############################################################
    # Should we add a new enemy?
    while (obs_index < len(obstacles_y)) and (player.s_y + s.HORIZON > obstacles_y[obs_index]):
        # Create the new enemy, and add it to our sprite groups
        new_enemy = Enemy(s_x = obstacles_x[obs_index], s_y = obstacles_y[obs_index])
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)
        
        obs_index += 1

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
    enemies.update(player.s_y)
    # clouds.update(player.v_y)

    collided = pygame.sprite.spritecollideany(player, enemies)
    # Check if any enemies have collided with the player
    if collided:
        # If so, remove the player
        player.penalize()
        
        collided.kill()
        crashes += 1
        # Stop any moving sounds and play the collision sound
        # move_up_sound.stop()
        # move_down_sound.stop()
        # collision_sound.play()

        # Stop the loop
        # running = False    

    # check winning condition
    if player.s_y > s.TRACK_LENGTH:
        finished = True
        running = False    

#RENDERING ############################################################
    # Fill the screen with sky blue
    red = max(0,min(255,player.v_y*5))
    window.fill((red, 255, 255-red))
    
    # Draw all our sprites
    for entity in all_sprites:
        window.blit(entity.surf, entity.rect)
    
    screen.fill(s.BLACK)
    screen.blit(window, ((s.SCREEN_WIDTH-s.WINDOW_WIDTH)/2, (s.SCREEN_HEIGHT-s.WINDOW_HEIGHT)/2))
    
    # pygame.draw.rect(window, RED, (0, 800, 0, 100))
    # Flip everything to the display
    pygame.display.update()

# END ############################################################
    tick += 1
    # Ensure we maintain a 30 frames per second rate
    clock.tick(s.FPS)
    print(f"fps: {clock.get_fps()}")
    
############################################################
    
print(f"reached the finish in {tick} ticks!")
print(f"Number of crashes: {crashes}")
print(f"Max speed reached: {player.max_speed} ticks!")
# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()



# Import the pygame module
import pygame
import time
import math
import sys
from entities import Player, Enemy, RoadMarker
import settings as s
from utils import try_quit, generate_obstacle_coords
import game as g

# import numpy as np

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *

# Initialize pygame
pygame.mixer.init()
pygame.init()
pygame.event.set_blocked ( pygame.MOUSEMOTION )
pygame.display.set_caption("Formula V")

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("assets/music/game.mp3")
pygame.mixer.music.play(loops=-1)

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

# Setup the clock for a decent framerate
clock = pygame.time.Clock()
screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))

game = g.Game(screen, clock)

# Our main loop
while game.running:
    
    for event in pygame.event.get():
        try_quit(event)

    game.update()
    
    if s.RENDER:
        game.render()
    

############################################################
    
print(f"reached the finish in {game.ticks} ticks!")
print(f"Number of crashes: {game.crashes}")
print(f"Max speed reached: {game.player.max_speed} pixels per second!")
# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()


# Import the pygame module
import pygame
import time
import math
import sys
from entities import Player, Enemy, RoadMarker
import settings as s
from utils import try_quit, generate_obstacle_coords
import game as g
import agent as a

# Initialize pygame

pygame.init()
pygame.event.set_blocked (pygame.MOUSEMOTION )
if s.SOUND:
    pygame.mixer.init()
if s.RENDER:
    screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
    pygame.display.set_caption("Formula V")

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

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


game = g.Game(screen, clock)
agent = a.Agent()

# Our main loop
while game.running:
    
    for event in pygame.event.get():
        try_quit(event)

    observation = game.observe()
    action = agent.act(observation)
    game.update(action)
    
    if s.RENDER:
        game.render()
    

############################################################
    
print(f"reached the finish in {game.ticks} ticks!")
print(f"Number of crashes: {game.crashes}")
print(f"Max speed reached: {game.player.max_speed} pixels per second!")


pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.display.quit()
pygame.quit()


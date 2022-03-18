# Import the pygame module
import pygame
import time
import settings as s
from utils import try_quit
import game as g
import agent as a

# Initialize pygame

pygame.init()
pygame.event.set_blocked (pygame.MOUSEMOTION )
if s.SOUND:
    pygame.mixer.init()
    pygame.mixer.music.load("assets/music/game.mp3")
    pygame.mixer.music.play(loops=-1)
if s.RENDER:
    pygame.display.set_caption("Formula V")
screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
clock = pygame.time.Clock()

# move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
# move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
# collision_sound = pygame.mixer.Sound("Collision.ogg")

# move_up_sound.set_volume(s.VOLUME)
# move_down_sound.set_volume(s.VOLUME)
# collision_sound.set_volume(s.VOLUME)

game = g.Game(screen, clock)
agent = a.Agent()

start_time = time.time()
while game.running:
    
    for event in pygame.event.get():
        try_quit(event)

    observation = game.observe()
    action = agent.act(observation)
    game.update(action)
    
    if s.RENDER:
        game.render()
        
        
end_time = time.time() - start_time   

print(f"Game completed in {end_time} seconds.")
print(f"reached the finish in {game.ticks} ticks!")
print(f"Number of crashes: {game.crashes}")
print(f"Max speed reached: {game.player.max_speed} pixels per second!")

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.display.quit()
pygame.quit()


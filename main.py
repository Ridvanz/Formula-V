# Import the pygame module
import pygame
import time
import settings as s
from utils import try_quit
import game as g
import agent as a

agent = a.Agent()

game = g.Game(0)

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




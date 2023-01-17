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
while not game.finished:

    observation = game.observe()

    print(observation)

    action = agent.act(observation)
    game.update(action)

    if s.RENDER:
        game.render()

end_time = time.time() - start_time

print(f"Game completed in {end_time} seconds.")
print(f"reached the finish in {game.ticks} ticks!")

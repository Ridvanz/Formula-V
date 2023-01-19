# Import the pygame module
# import pygame
import time
import settings as s
import game as g
import agent as a

agent = a.Agent()

game = g.Game(seed=0, render_mode = True)

start_time = time.time()
while not game.finished:

    observation = game.observe()

    action = agent.act(observation)
    game.update(action)

    if game.render_mode:
        game.render()

end_time = time.time() - start_time

print(f"Game completed in {end_time} seconds.")
print(f"reached the finish in {game.ticks} ticks!")
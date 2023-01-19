# Import the pygame module
# import pygame
import time
import src.settings as s
import src.game as g
import agent as a

agent = a.Agent()

game = g.Game(seed=0, render_mode = True)
# game = g.Game(seed=0, render_mode = False)

start_time = time.time()
while not game.finished:

    observation = game.observe()

    action = agent.act(observation)
    game.update(action)

    if game.render_mode:
        game.render()

end_time = time.time() - start_time

print(f"Game completed in {end_time} seconds.")
print(f"Traveled a distance {game.player[1]} units.")
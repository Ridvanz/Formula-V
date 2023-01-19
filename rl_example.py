import gymnasium as gym
from gym_env import FormulaVEnv

env = FormulaVEnv()

observation, info = env.reset(seed=42)

for _ in range(1000):
    action = env.action_space.sample()
    
    print(action)
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()
        
env.close()

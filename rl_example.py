#%%
import sys
import gymnasium
import gymnasium
sys.modules["gym"] = gymnasium
from gymnasium import spaces
import src.game as g
import time
import numpy as np

class FormulaVEnv(gymnasium.Env):
    
    def __init__(self, render_mode=False):
        super().__init__()
        
        self.render_mode = render_mode
        self.observation_space = spaces.Box(-1.0, 1.0, shape=(19,),  dtype=np.float32)
        self.action_space = spaces.Box(-1.0, 1.0, shape=(2,), dtype=np.float32)

    def _get_obs(self):
        
        observation = self.game.observe()
        observation[1:,0] -= observation[0,0] #make x pos of obstacles relative to player
        observation = np.delete(observation.flatten(),1)   
        observation = np.float32(observation)
   
        return observation

    def _get_info(self):
        return {
            "ticks": self.game.ticks
        }

    def reset(self, seed=None):
        super().reset(seed=seed)

        self.game = g.Game(seed=seed)

        if self.render_mode:
            self.render()
            
        observation = self._get_obs()

        return observation

    def step(self, action):

        self.game.update(action)
        terminated = self.game.finished
        observation = self._get_obs()
        info = self._get_info()

        #reward the forward speed of the player
        reward  = float(observation[2])

        if self.render_mode:
            self.render()

        return observation, reward, terminated, info

    def render(self):
        self.game.render()
        
    def close(self):
        self.game.stop()

from stable_baselines3 import PPO, A2C
from stable_baselines3.common.env_checker import check_env

if __name__ == '__main__':
    
    env = FormulaVEnv(render_mode = False)
    observation = env.reset(seed=42)
    
    model = A2C("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    model.save("ppo_formulav")
    
    # model = PPO.load("ppo_formulav")
    
    env = FormulaVEnv(render_mode = True)
    observation = env.reset(seed=42)
    time1 = time.perf_counter()
    
    terminated = False
    action_history = []
    
    while not terminated:
        # action = env.action_space.sample()
        action, _states = model.predict(observation)

        observation, reward, terminated, info = env.step(action)

        action_history.append(action)

    end_time = time.perf_counter() - time1
    
    print(np.stack(action_history))
    
    print(f"Game completed in {end_time} seconds.")
    print(f"Traveled a distance {env.game.player[1]} units.")
    
    env.close()
    
    
   
   
#%%
import sys
import gymnasium
import gymnasium
sys.modules["gym"] = gymnasium
from gymnasium import spaces
import game as g
import time
import numpy as np

class FormulaVEnv(gymnasium.Env):
    
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, render_mode=None):
        super().__init__()
        
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        
        # self.observation_space = spaces.Dict(
        #     {
        #         "agent": spaces.Box(0, 2, shape=(2,), dtype=int),
        #         "target": spaces.Box(0, 2, shape=(2,), dtype=int),
        #     }
        # )
        
        self.observation_space = spaces.Box(-1.0, 1.0, shape=(19,),  dtype=np.float32)

        self.action_space = spaces.Box(-1.0, 1.0, shape=(2,), dtype=np.float32)

    def _get_obs(self):
        
        state = self.game.observe()
        
        observation = np.concatenate([state["player"][[0,2,3]], state["obstacles"].flatten()],0)
        observation = np.float32(observation)
        # print(observation.shape)
        return observation

    def _get_info(self):
        return {
            "distance": self.game.ticks
        }

    def reset(self, seed=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.game = g.Game(seed=seed)


        # info = self._get_info()

        if self.render_mode == "human":
            self.render()
            
        observation = self._get_obs()
        # print(observation)

        return observation

    def step(self, action):

        self.game.update(action)
        # An episode is done iff the agent has reached the target
        terminated = self.game.finished
        
        observation = self._get_obs()
        info = self._get_info()

        reward  = float(observation[2])

        
        if self.render_mode == "human":
            self.render()

        return observation, reward, terminated, info

    def render(self):
        self.game.render()
        
    def close(self):
        self.game.stop()


from stable_baselines3 import PPO, A2C
from stable_baselines3.common.env_checker import check_env

if __name__ == '__main__':
    
    # env = FormulaVEnv(render_mode = "human")
    env = FormulaVEnv(render_mode = None)
    observation = env.reset(seed=42)
    print(observation)
    
    model = A2C("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=100_000)
    model.save("ppo_formulav")
    
    # model = PPO.load("ppo_formulav")
    
    observation = env.reset(seed=42)
    time1 = time.perf_counter()
    
    while not env.game.stopped:
        # action = env.action_space.sample()
        action, _states = model.predict(observation)

        observation, reward, terminated, info = env.step(action)

        if terminated:
            observation = env.reset()
        
        env.render()
            
    print('time: {}'.format(time.perf_counter() - time1))
    
    env.close()
    
    
# # Instantiate the env
# env = CustomEnv(arg1, ...)
# # Define and Train the agent
# model = A2C("CnnPolicy", env).learn(total_timesteps=1000)




# from gym.envs.registration import register
# # Example for the CartPole environment
# register(
#     # unique identifier for the env `name-version`
#     id="CartPole-v1",
#     # path to the class for creating the env
#     # Note: entry_point also accept a class as input (and not only a string)
#     entry_point="gym.envs.classic_control:CartPoleEnv",
#     # Max number of steps per episode, using a `TimeLimitWrapper`
#     max_episode_steps=500,
# )

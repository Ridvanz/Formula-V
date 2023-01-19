import numpy as np
from numba import njit
import time

N = 8
size = 0.05

@njit()
def set_seed(value):
    np.random.seed(value)

@njit()
def get_initial_state():

    idx = 0
    player_x = 0.5
    player_y = 0
    player_vx = 0
    player_vy = 0
    
    player = np.array([player_x, player_y, player_vx, player_vy])
    
    enemy_x = np.random.rand(N)
    enemy_y = np.linspace(0,2,N+1)[:-1] + 2/N
    enemy_vx = np.random.rand(N)*2-1
    enemy_active = np.ones(N)
    obstacles = np.stack((enemy_x, enemy_y, enemy_vx, enemy_active),1)

    passed = int(obstacles[idx, 1] < -size)
    items = [(idx + i + passed)%N for i in range(4)]
    state = [player]+[obstacles[item,:] for item in items]
    
    observation = np.empty((5,4))
    
    for i in range(5):
        observation[i,:] = state[i]
    
    return player, obstacles, idx, observation
  
@njit(fastmath=True)
def game_update(u, player, obstacles, idx):
    
    C_x, C_y, C_r, C_p = 0.95, 0.9995, 0.99, 0.5

    u_x, u_y = u
    u_x = max(-1, min(u_x, 1))
    u_y = max(-1, min(u_y, 1))

    a_x  = u_x * 0.001
    a_y  = u_y * 0.00005

    player[2] =  C_x * player[2] + a_x
    player[3] = max(0, C_y * player[3] + a_y)
    
    player[0] =  player[0] +  player[2]
    player[1] =  player[1] +  player[3]
    
    if player[0]<0:
        player[0] = 0
        player[2] *= -C_r
    elif player[0]>1:
        player[0] = 1
        player[2] *= -C_r
    
    obstacles[:,1] -= player[3]
    
    obstacles[:,0] += 0.02*obstacles[:,2]
    obstacles[(obstacles[:,0]<0) | (obstacles[:,0]>1), 2] *= -1
    
    if obstacles[idx,1] < -2*size:
        
        obstacles[idx,0] = np.random.rand()
        obstacles[idx,1] += 2
        obstacles[idx,2] = np.random.rand()*2-1
        obstacles[idx,3] = 1
        
        idx = (idx+1)%N
        
    if abs(obstacles[idx,1]) < size and (abs(obstacles[idx,0]-player[0]) < size) and obstacles[idx,3]:
        obstacles[idx,3] = 0
        player[3] *= C_p
    
    passed = int(obstacles[idx, 1] < -size)
    items = [(idx + i + passed)%N for i in range(4)]
    state = [obstacles[item,:] for item in items]
    
    observation = np.empty((5,4))
    observation[0,:] = player
    
    for i in range(4):
        observation[i+1,:] = state[i]
        
    # print(observation)
    return player, obstacles, idx, observation

if __name__ == '__main__':
    
    set_seed(0)

    player, obstacles, idx, observation = get_initial_state()

    observation_history =[]
    
    time1 = time.perf_counter()

    for i in range(600000):
        
        u = (0,1)
        player, obstacles, idx, observation  = game_update(u, player, obstacles, idx)

        observation_history.append(observation.copy())

    print('time: {}'.format(time.perf_counter() - time1))

    data = np.stack(observation_history)

    # print(observation_history[10])
import numpy as np
from numba import njit
import time

def get_initial_state():

    N = 5
    idx = 0
    player_x = 0.5
    player_y = 0
    player_vx = 0
    player_vy = 0
    
    player = np.array([player_x, player_y, player_vx, player_vy])
    
    enemy_x = np.random.rand(N)
    enemy_y = np.linspace(0,2,N, endpoint=False)
    enemy_vx = np.random.rand(N)*2-1
    enemy_active = np.ones(N)
    enemies = np.stack([enemy_x, enemy_y, enemy_vx, enemy_active],1)
    
    return player, enemies, idx
  
  
@njit(fastmath=True)
def game_update(u, player, enemies, idx):
    
    N=5
    size = 0.05
    C_x, C_y, C_r, C_p = 0.9, 0.9995, 0.9, 0.5

    u_x, u_y = u
    u_x = max(-1, min(u_x, 1))
    u_y = max(-1, min(u_y, 1))

    a_x  = u_x * 0.001
    a_y  = u_y * 0.0001

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
    
    enemies[:,1] -= player[3]
    
    enemies[:,0] += 0.01*enemies[:,2]
    enemies[(enemies[:,0]<0) | (enemies[:,0]>1), 2] *= -1
    
    if enemies[idx,1] < -size:
        
        enemies[idx,0] = np.random.rand()
        enemies[idx,1] += 2
        enemies[idx,2] = np.random.rand()*2-1
        enemies[idx,3] = 1
        
        idx = (idx+1)%N
        
    if abs(enemies[idx,1]) < size and (abs(enemies[idx,0]-player[0]) < size) and enemies[idx,3]:
        enemies[idx,3] = 0
        player[3] *= C_p
    
    return player, enemies, idx




# player, enemies, idx = get_initial_state()

# u = (0,1)

# players =[]
# enemiess = []
# time1 = time.perf_counter()

# for i in range(6000):
    
#     player, enemies, idx = game_update(u, player, enemies, idx)

#     players.append(player.copy())
#     enemiess.append(enemies.copy())

# print('time: {}'.format(time.perf_counter() - time1))

# player_data = np.stack(players)
# enemy_data = np.stack(enemiess)

# print(player_data)
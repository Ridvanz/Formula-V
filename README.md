# Formula-V
 
##About

Formula V is a top-down hyper realistic racing simulator. It serves as an Agent-Environment interface for showcasing algorithms and strategies in autonomous navigation. The project was developed by consultants from Vantage AI for an internal competition.

##Installation

install the required packages with "pip install requirements"
For those who wish to try reinforcement learning, you can additionally install "pip install requirements_rl"

##Running the game

The game can be played by running the main.py file in the root folder. When we initialize the game with render_mode = True,
a window opens where you can visualize and play the game yourself.

##Gameplay

The movements of the car are controlled by two input variables: u_x and u_y. Both have to be in range (-1,1)
The inputs represent the accelerations of the car in both the horizontal and vertical directions:
```
        a_x = u_x * scale_x
        a_y = u_y * scale_y
```
The velocity of the car is given by:
```
        v_x = C_x * v_x + a_x
        v_y = C_y * v_y + a_y 
```
Where C_x and C_y serve as friction coefficients in the x and y directions respectively.

Hitting an obstacle or a wall incurs additional penalties on the velocities.

The inputs can be supplied by either pressing the direction keys or WASD when rendering is turned on, or by the act function of the Agent class. 

The Agent.act function takes as input the state of the environment, which includes information about the player and currently instantiated obstacles, and returns the control inputs u_x and u_y. Your assignment is to rewrite this class such that the car navigates through the obstacles as fast a possible. The score is equal to the distance traveled (player_y) after 3600 ingame ticks (60 seconds). 

##Observations
The game.observe method returns a numpy array containing the current states of the onscreen objects that you may use to control the agent. Here is an example of an observation:

[[ 0.5         0.00658901  0.          0.00109725]
 [ 0.75282512  0.24341099  0.92732552  1.        ]
 [ 0.66390363  0.49341099 -0.23311696  1.        ]
 [ 0.73112239  0.74341099  0.58345008  1.        ]
 [ 0.55759695  0.99341099  0.05778984  1.        ]]

The first row contains data of the player in the following format:

 [player_x [range(0,1)], player_y [range(0,inf)], player_vx [range(-1,1)], player_vy [range(0,0.02)]]
 
where x is the x-coordinate and vx is the speed in the horitontal direction etc.

The second to last rows contain variables about the obstacles on the screen in the following format

 [obstacle_x [range(0,1)], obstacle_y [range(-0.1,1)], obstacle_vx [range(-1,1)], obstacle_exist [bool]]
 
Note that the y coordinate of the obstacles are relative to the player. Also, the obstacles dont move vertically. The variable obstacle_exist turns to 0 if it has been hit by the player, after which it cant be hit again. 


##Settings
The values in src/settings.py can be altered to suit your needs. For example, you van tweak the window and screen sizes to your liking. Or turn off that anoying background music. This wont affect gameplay.

##Further info

For reinforcement learning algorithms I suggest using this package for out of the box compatibility with the gym environment:
https://github.com/DLR-RM/stable-baselines3

The recent version of the game is refactored with numba for a 1000x speedup.
The src/simulate.py file contains the core numba functions that implement the game logic. 
You could potentially use these to efficiently generate a lot of input/output data without the overhead of the pygame class.
An example is given when you run the script.
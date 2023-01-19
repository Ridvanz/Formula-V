# Formula-V
 
##About

Formula V is a top-down racing simulator. It serves as an Agent-Environment interface for showcasing basic algorithms and strategies in autonomous navigation. The project was developed by consultants from Vantage AI for use during a Hackaton.

##Installation

To play, ensure that you have [Python 3.x](https://www.python.org/) and [Pygame](http://www.pygame.org/download.shtml) installed, and then:

```
  $ ./play
```

##Settings
The values in settings.py can be altered to suit your needs. For example, we can set RENDERING = False to greatly speed up the simulation.

##Gameplay

The movements of the car are controlled by two input variables: u_x and u_y.
These inputs can be supplied by either pressing the direction keys, or by the act function of the Agent class. Your assignment is to rewrite this class such that the car navigates through the obstacles as fast a possible.

The Agent.act function takes as input the state of the environment, which includes information about the player and currently instantiated obstacles, and returns the control inputs u_x and u_y.

State variables:
- Distance from player to left wall
- Distance from player to right wall
- Distance traveled
- Current player velocity in the X direction
- Current player velocity in the Y direction
- For each obstacle on the screen
  - Relative x position to player
  - Relative y position to player

The inputs are scaled to represent the accelerations of the car in both the horizontal and vertical directions:

```
        a_x = u_x * scale_x
        a_y = u_y * scale_y
```
The velocity of the car is then given by:
```
        v_x = C_x * v_x + a_x
        v_y = C_y * v_y + a_y 
```
Where C_x and C_y serve as friction coefficients in the x and y directions respectively.

Hitting an obstacle or a wall incurs additional penalties on the velocities.

The goal of the game is to reach the finish in as few game ticks as possible. 

For reinforcement learning algorithms I suggest using this package for out of the box compatibility:
https://github.com/DLR-RM/stable-baselines3


Refactored the game logic with numba for a 1000x speedup!
The first function call to game_update takes about a second to compile. 
After that, we can run about 600,000 game updates per second.


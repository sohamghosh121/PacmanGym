# OpenAI Gym Berkeley-Pacman 

Port of Berkeley AI Pacman to an OpenAI Gym environment.

The Berkeley Pacman AI engine is provided at http://ai.berkeley.edu/project_overview.html

## Info
This repository provides two environments:
* **BerkeleyPacman-v0**: which provides the Berkeley Pacman AI interface as is, with a randomly chosen layout. Layouts are in layouts/ folder
* **BerkeleyPacmanPO-v0**: which provides the Berkeley Pacman AI interface with only a partially observable portion of the map (immediate nearby locations in a 3x3 grid)

## Usage
To use these environments, do:
~~~~
import gym
import gym_pacman
env = gym.make('BerkeleyPacman-v0')
~~~~

Note: This was created for the 10-703 Project at Carnegie Mellon University. This is still under active development

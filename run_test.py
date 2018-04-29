from PIL import Image
import gym
import gym_pacman
import time

env = gym.make('BerkeleyPacmanPO-v0')
env.seed(1)


done = False
i = 0
while True:
    done = False
    env.reset()
    while not done:
        i += 1
        s_, r, done, info = env.step(env.action_space.sample())
        env.render()
        
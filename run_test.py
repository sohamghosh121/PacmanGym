from PIL import Image
import gym
import gym_pacman
env = gym.make('BerkeleyPacmanPO-v0')
import time
done = False
i = 0
env.reset()
while True:
    done = False
    env.reset()
    while not done:
        i += 1
        s_, r, done, info = env.step(env.action_space.sample())
        env.render()
        
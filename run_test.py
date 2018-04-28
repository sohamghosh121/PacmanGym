from PIL import Image
import gym
import gym_pacman
env = gym.make('BerkeleyPacmanPO-v0')
import time
done = False
i = 0
env.reset(layout='contestClassic_noGhosts')
while i < 60:
    i += 1
    s_, r, done, info = env.step(env.action_space.sample())
    env.render()
    print(r, done, info)
# Image.fromarray(s_).save("hi_%d.png" % i)
    
from PIL import Image
import gym
import gym_pacman
e = gym.make('BerkeleyPacmanPO-v0')

done = False
i = 0
print(e.observation_space)
e.reset(layout='contestClassic')
while not done:
    i += 1
    s_, r, done, info = e.step(e.action_space.sample())
    print(r, done, info, s_.shape)
    Image.fromarray(s_).save("hi_%d.png" % i)

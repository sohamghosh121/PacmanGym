from PIL import Image
import gym
import gym_pacman
env = gym.make('BerkeleyPacmanPO-v0')

done = False
i = 0
env.reset(layout='contestClassic_noGhosts')
while not done:
    i += 1
    s_, r, done, info = env.step(env.action_space.sample())
    env.render()
    print(r, done, info, s_.shape)
    Image.fromarray(s_).save("hi_%d.png" % i)
    
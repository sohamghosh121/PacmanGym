import gym
from gym import spaces
from gym.utils import seeding
import numpy as np

import graphicsDisplay as gd
from graphicsDisplay import DEFAULT_GRID_SIZE

from game import Actions
from pacman import ClassicGameRules
from layout import getLayout

from ghostAgents import DirectionalGhost
from pacmanAgents import OpenAIAgent

DEFAULT_GHOST_TYPE = 'DirectionalGhost'

MAX_GHOSTS = 5

PACMAN_ACTIONS = ['North', 'South', 'East', 'West', 'Stop']

PACMAN_DIRECTIONS = ['North', 'South', 'East', 'West']
ROTATION_ANGLES = [0, 180, 90, 270]

class PacmanEnv(gym.Env):
    layouts = [
        'capsuleClassic', 'contestClassic', 'mediumClassic', 'mediumGrid', 'minimaxClassic', 'openClassic', 'originalClassic', 'smallClassic', 'capsuleClassic', 'smallGrid', 'testClassic', 'trappedClassic', 'trickyClassic'
    ]

    noGhost_layouts = [l + '_noGhosts' for l in layouts]

    MAX_MAZE_SIZE = (45, 45)

    def __init__(self):
        self.chooseLayout()
        self.action_space = spaces.Discrete(4) # up, down, left right
        self.display = gd.PacmanGraphics(1.0)
        self.setObservationSpace()
        self._action_set = range(len(PACMAN_ACTIONS))
        self.location = None
        self.reset()

    def setObservationSpace(self):
        screen_width, screen_height = self.display.calculate_screen_dimensions(self.layout.width,   self.layout.height)
        self.observation_space = spaces.Box(low=0, high=255,
            shape=(int(screen_height),
                int(screen_width),
                3), dtype=np.uint8)

    def chooseLayout(self, chosenLayout=None, no_ghosts=True):
        if chosenLayout is None:
            if not no_ghosts:
                chosenLayout = np.random.choice(self.layouts)
            else:
                chosenLayout = np.random.choice(self.noGhost_layouts)
        self.chosen_layout = chosenLayout
        print "Chose layout", chosenLayout
        self.layout = getLayout(chosenLayout)
        self.maze_size = (self.layout.width, self.layout.height)

    def reset(self, layout=None):
         # get new layout
        self.chooseLayout(layout)
        self.setObservationSpace()

        self.ghosts = [DirectionalGhost( i+1 ) for i in range(MAX_GHOSTS)]

        # this agent is just a placeholder for graphics to work
        self.pacman = OpenAIAgent()

        self.rules = ClassicGameRules(300)
        self.rules.quiet = False

        self.game = self.rules.newGame(self.layout, self.pacman, self.ghosts,
            self.display, False, False)

        self.game.init()

        self.display.initialize(self.game.state.data)
        self.display.updateView()

        self.location = self.game.state.data.agentStates[0].getPosition()
        self.location_history = [self.location]
        self.orientation = PACMAN_DIRECTIONS.index(self.game.state.data.agentStates[0].getDirection())
        self.orientation_history = [self.orientation]
        self.illegal_move_counter = 0
        return self._get_image()

    def step(self, action):
        # implement code here to take an action
        pacman_action = PACMAN_ACTIONS[action]

        legal_actions = self.game.state.getLegalPacmanActions()
        illegal_action = False
        if pacman_action not in legal_actions:
            self.illegal_move_counter += 1
            illegal_action = True
            pacman_action = 'Stop' # Stop is always legal

        reward = self.game.step(pacman_action)

        # reward shaping for illegal actions
        if illegal_action:
            reward -= 10

        done = self.game.state.isWin() or self.game.state.isLose()

        self.location = self.game.state.data.agentStates[0].getPosition()
        self.location_history.append(self.location)

        self.orientation = PACMAN_DIRECTIONS.index(self.game.state.data.agentStates[0].getDirection())
        self.orientation_history.append(self.orientation)

        info = {
            'past_loc': self.location_history[-2],
            'curr_loc': self.location_history[-1],
            'past_orientation': self.orientation_history[-2],
            'curr_orientation': self.orientation_history[-1],
            'illegal_move_counter': self.illegal_move_counter
        }

        return self._get_image(), reward, done, info

    def get_action_meanings(self):
        return [PACMAN_ACTIONS[i] for i in self._action_set]

    def _get_image(self):
        image = self.display.image
        return np.array(image)

    def render(self, mode='human'):
        img = self._get_image()
        if mode == 'rgb_array':
            return img
        elif mode == 'human':
            from gym.envs.classic_control import rendering
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
            return self.viewer.isopen

    def close(self):
        # implement code here to do closing stuff
        self.display.finish()
        vdisplay.stop()


class PartiallyObservablePacmanEnv(PacmanEnv):

    # just change the get image function
    def _get_image(self):
        # get x, y
        image = self.display.image
        
        w, h = image.size
        DEFAULT_GRID_SIZE_X, DEFAULT_GRID_SIZE_Y = w / float(self.layout.width), h / float(self.layout.height)

        extent = [
            DEFAULT_GRID_SIZE_X *  (self.location[0] - 1.5),
            DEFAULT_GRID_SIZE_Y *  (self.layout.height - (self.location[1] + 2.5)),
            DEFAULT_GRID_SIZE_X *  (self.location[0] + 2.5),
            DEFAULT_GRID_SIZE_Y *  (self.layout.height - (self.location[1] - 1.5))]


        extent = tuple([int(e) for e in extent])
        image = image.crop(extent).resize((84, 84))
        return np.array(image)

    def setObservationSpace(self):
        self.observation_space = spaces.Box(low=0, high=255,
            shape=(84, 84, 3), dtype=np.uint8)


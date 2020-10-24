import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np


class AccessControlEnv(gym.Env):
    def __init__(self):
        # Env constants
        self.N_SERVERS = 10
        self.FREE_SERVER_PROB = 0.06
        self.PRIORITIES = [1, 2, 4, 8]

        # Gym
        self.action_space = spaces.Discrete(2)  # Accept or reject
        self.observation_space = spaces.Discrete(2)  # spaces.Box((0, self.PRIORITIES[0]), (self.N_SERVERS, self.PRIORITIES[-1]))  # (free_servers, curr_priority)

    def step(self, action):
        # Parse action
        # reject = 0
        # accept = 1
        accept = bool(action)

        # Accept (only if server available)
        if accept and self.free_servers > 0:
            # Compute reward
            reward = self.curr_priority
            # Decrement free servers
            self.free_servers -= 1
            # Get next priority
            self.curr_priority = np.random.choice(self.PRIORITIES)
        else: # Reject
            reward = 0

        # Free server
        if np.random.sample() <= self.FREE_SERVER_PROB and self.free_servers < self.N_SERVERS:
            self.free_servers += 1

        return (self.free_servers, self.curr_priority), reward, False, {}

    def reset(self):
        self.free_servers = self.N_SERVERS
        self.curr_priority = np.random.choice(self.PRIORITIES)
        return (self.free_servers, self.curr_priority)

    def render(self):
        pass

    def close(self):
        pass

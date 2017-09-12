
import numpy as np

class Player(object):
    def __init__(self, environment):
        self.position = np.zeros((0, 2))  # meters
        self.speed = 0  # m/s
        self.isStatic = True  #
        self.environment = environment

class Detector(Player):
    def __init__(self, environment=None, speed=None, path=None):
        super().__init__()

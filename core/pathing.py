
import numpy as np
from itertools import repeat


class Plan(object):

    def __init__(self, listofobjects, time_step):
        self.object_list = listofobjects
        self.time_step = time_step
        self.fill_in_the_gaps()

    def fill_in_the_gaps(self):
        # self.time = np.ndarray((0,))
        # self.position = np.ndarray((0, 2))
        # self.orientation = np.ndarray((0,))
        self.segments = []
        self.color = []
        for i in range(len(self.object_list)):
            # skip the first one
            if i == 0:
                continue
            current = self.object_list[i]
            previous = self.object_list[i-1]
            # now to fill in how I got here.
            dt = current.time - previous.time
            time_steps_needed = int(dt / self.time_step)
            time = np.linspace(previous.time, current.time, time_steps_needed)
            position = np.zeros((time_steps_needed, 2))
            position[:, 0] = np.linspace(previous.position['meters'][0],
                                         current.position['meters'][0],
                                         time_steps_needed)
            position[:, 1] = np.linspace(previous.position['meters'][1],
                                         current.position['meters'][1],
                                         time_steps_needed)
            orientation = previous.orientation
            color = current.color
            self.segments += [{'time': time, 'position': position, 'orientation': orientation,
                               'color': color}]



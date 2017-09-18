
import sys
sys.path.append('/home/holiestcow/Documents/2017_fall/ne697_hayward')

import numpy as np
from radsynth.core.items import Detector
from itertools import repeat


class Plan(object):

    def __init__(self, listofobjects, time_step):
        self.object_list = listofobjects
        self.template_object = listofobjects[0]
        self.time_step = time_step
        self.fill_in_the_gaps()
        self.construct_full_object_list()
        return

    def get_refined_object_list(self):
        return self.refined_object_list

    def distance_between(self, coord1, coord2):
        distance = np.linalg.norm(coord1 - coord2)
        return distance

    def angle_between(self, coord1, coord2):
        # Angle of object2 relative to object1
        dpos = coord2 - coord1
        angle = (np.rad2deg(np.arctan(dpos[0] / dpos[1])))
        return angle

    def fill_in_the_gaps(self):
        # self.time = np.ndarray((0,))
        # self.position = np.ndarray((0, 2))
        # self.orientation = np.ndarray((0,))
        self.segments = {}
        self.segments['name'] = []
        self.segments['time'] = np.ndarray((0,))
        self.segments['position'] = np.ndarray((0, 2))
        self.segments['orientation'] = np.ndarray((0,))
        self.segments['speed'] = np.ndarray((0,))
        self.segments['color'] = []
        self.color = []
        counter = 0
        for i in range(len(self.object_list)):
            # skip the first one
            if i == 0:
                continue
            current = self.object_list[i]
            previous = self.object_list[i - 1]
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
            speed = np.repeat((self.distance_between(current.position['meters'],
                                                     previous.position['meters']) / dt),
                              time_steps_needed, axis=0)
            position_label = np.arange(counter, counter + time_steps_needed)
            counter = counter + position_label[-1]
            labels = []
            for j in range(len(position_label)):
                labels += ['{}_{}'.format(self.object_list[i].name, position_label[j])]
            # orientation = np.array(list(repeat(previous.orientation, time_steps_needed)))
            # orientation = np.repeat(previous.orientation, time_steps_needed, axis=0)
            orientation = np.repeat(self.angle_between(current.position['meters'],
                                                       previous.position['meters']),
                                    time_steps_needed, axis=0)
            # print(orientation.shape)
            color = list(repeat(current.color, time_steps_needed))
            # self.segments += {'name': labels, 'time': time, 'position': position, 'orientation': orientation,
                            #   'color': color}
            self.segments['name'] += labels
            # print(self.segments['time'].shape, time.shape)
            self.segments['time'] = np.concatenate((self.segments['time'], time),
                                                   axis=0)
            self.segments['position'] = np.concatenate((self.segments['position'], position),
                                                       axis=0)
            self.segments['orientation'] = np.concatenate((self.segments['orientation'], orientation),
                                                          axis=0)
            self.segments['speed'] = np.concatenate((self.segments['speed'], speed),
                                                    axis=0)
            self.segments['color'] += color
        return

    def construct_full_object_list(self):
        self.refined_object_list = []
        for i in range(len(self.segments['name'])):
            self.refined_object_list += [Detector(name=self.segments['name'][i],
                                                  position=self.segments['position'][i, :],
                                                  material=self.template_object.material,
                                                  detector_number=self.template_object.detector_number,
                                                  orientation=self.segments['orientation'][i],
                                                  speed=self.segments['speed'][i],
                                                  time=self.segments['time'][i],
                                                  color=self.segments['color'][i])]
        return



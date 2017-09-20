
import sys
sys.path.append('/home/holiestcow/Documents/2017_fall/ne697_hayward')

import numpy as np
from radsynth.core.items import Detector
from itertools import repeat, compress


class Plan(object):

    def __init__(self, listofobjects, time_step, sub_time_step):
        self.object_list = listofobjects
        self.template_object = listofobjects[0]
        self.time_step = time_step
        self.sub_time_step = sub_time_step
        self.fill_in_the_gaps()
        self.construct_object_lists()
        return

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
        self.sub_segments = {}
        self.sub_segments['name'] = []
        self.sub_segments['time'] = np.ndarray((0,))
        self.sub_segments['position'] = np.ndarray((0, 2))
        self.sub_segments['orientation'] = np.ndarray((0,))
        self.sub_segments['speed'] = np.ndarray((0,))
        self.sub_segments['color'] = []
        self.color = []
        counter = 0
        total_sub_time_steps_needed = 0
        for i in range(len(self.object_list)):
            # skip the first one
            if i == 0:
                continue
            current = self.object_list[i]
            previous = self.object_list[i - 1]
            # now to fill in how I got here.
            dt = current.time - previous.time
            sub_time_steps_needed = int(dt / self.sub_time_step)
            total_sub_time_steps_needed += sub_time_steps_needed
            time = np.linspace(previous.time, current.time, sub_time_steps_needed+1)
            position = np.zeros((sub_time_steps_needed, 2))
            position[:, 0] = np.linspace(previous.position['meters'][0],
                                         current.position['meters'][0],
                                         sub_time_steps_needed)
            position[:, 1] = np.linspace(previous.position['meters'][1],
                                         current.position['meters'][1],
                                         sub_time_steps_needed)
            speed = np.repeat((self.distance_between(current.position['meters'],
                                                     previous.position['meters']) / dt),
                              sub_time_steps_needed, axis=0)
            position_label = np.arange(counter, counter + sub_time_steps_needed)
            counter = counter + position_label[-1]
            labels = []
            for j in range(len(position_label)):
                labels += ['{}_{}'.format(self.object_list[i].name, position_label[j])]
            # orientation = np.array(list(repeat(previous.orientation, sub_time_steps_needed)))
            # orientation = np.repeat(previous.orientation, sub_time_steps_needed, axis=0)
            orientation = np.repeat(self.angle_between(current.position['meters'],
                                                       previous.position['meters']),
                                    sub_time_steps_needed, axis=0)
            # print(orientation.shape)
            color = list(repeat(current.color, sub_time_steps_needed))
            self.sub_segments['name'] += labels
            self.sub_segments['time'] = np.concatenate((self.sub_segments['time'], time),
                                                       axis=0)
            self.sub_segments['position'] = np.concatenate((self.sub_segments['position'],
                                                           position), axis=0)
            self.sub_segments['orientation'] = np.concatenate((self.sub_segments['orientation'],
                                                              orientation), axis=0)
            self.sub_segments['speed'] = np.concatenate((self.sub_segments['speed'], speed),
                                                        axis=0)
            self.sub_segments['color'] += color

        start_time = self.sub_segments['time'][0]
        end_time = self.sub_segments['time'][-1]
        # TODO: Assert every_nth_step and time_steps needed are perfect integers.
        #       If not, raise value error or compensate.
        #       This will occur when the waypoint times aren't perfectly divisible
        #       by the sub_time_step value.
        time_steps_needed = int((end_time - start_time) / self.time_step)
        every_nth_step = int(total_sub_time_steps_needed / time_steps_needed)
        # time_observed = np.linspace(start_time, end_time, time_steps_needed)
        self.segments = {}
        self.segments['time'] = self.sub_segments['time'][::every_nth_step]
        self.segments['position'] = self.sub_segments['position'][::every_nth_step]
        self.segments['orientation'] = self.sub_segments['orientation'][::every_nth_step]
        self.segments['speed'] = self.sub_segments['speed'][::every_nth_step]
        self.segments['color'] = self.sub_segments['color'][::every_nth_step]
        template_name = self.template_object.name
        self.segments['name'] = []
        self.segments['sub_segments'] = []
        for i in range(time_steps_needed):
            self.segments['name'] += ['{}_position{}'.format(template_name, i)]
            if i == 0:
                # First detector waypoint won't get any sub segments
                self.segments['sub_segments'].append([])
                time_keeper = self.segments['time'][i]
                continue
            # TODO: Assign ownership mask such that the invisible detectors feed the measurement
            # for the observed detectors. It seems we're constructing 2 seperate detector object
            # lists: invisible and observed detectors.
            # HAs to happen outside of segment construction.'
            mask1 = self.sub_segments['time'] <= self.segments['time'][i]
            mask2 = self.sub_segments['time'] > time_keeper
            desired_mask = mask1 & mask2
            # self.segments['sub_segments'] = np.concatenate((
            #     self.segments['sub_segments'], desired_mask), axis=0)
            self.segments['sub_segments'] += [desired_mask]
            time_keeper = self.segments['time'][i]
        return

    def construct_object_lists(self):
        self.physical_object_list = []
        for i in range(len(self.sub_segments['name'])):
            self.physical_object_list += [Detector(name=self.sub_segments['name'][i],
                                                   position=self.sub_segments['position'][i, :],
                                                   material=self.template_object.material,
                                                   detector_number=self.template_object.detector_number,
                                                   orientation=self.sub_segments['orientation'][i],
                                                   speed=self.sub_segments['speed'][i],
                                                   time=self.sub_segments['time'][i],
                                                   color=self.sub_segments['color'][i])]
        self.observed_object_list = []
        self.detector_observed2physical = {}
        print(len(self.segments['name']), len(self.segments['sub_segments']))
        for i in range(len(self.segments['name'])):
            self.observed_object_list += [Detector(name=self.segments['name'][i],
                                                   position=self.segments['position'][i, :],
                                                   material=self.template_object.material,
                                                   detector_number=self.template_object.detector_number,
                                                   orientation=self.segments['orientation'][i],
                                                   speed=self.segments['speed'][i],
                                                   time=self.segments['time'][i],
                                                   color=self.segments['color'][i])]
            # self.detector_observed2physical[self.segments['name'][i]] = \
            mask = self.segments['sub_segments'][i]
            self.detector_observed2physical[self.segments['name'][i]] = \
                [compress(self.physical_object_list, mask)]


        # construct the observed object list with grouped detector objects.
        return



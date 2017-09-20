

import sys
sys.path.append('/home/holiestcow/Documents/2017_fall/ne697_hayward')

from radsynth.core.playground import Playground
from radsynth.core.items import Detector, Source
import numpy as np


def main():

    # Define items
    cs137_1 = Source(name='cs137_1', position=np.array([20, 20]), isotope='cs137',
                     activity_mCi=1)
    cs137_2 = Source(name='cs137_2', position=np.array([-25, -35]), isotope='cs137',
                     activity_mCi=0.25)
    # NOTE: Have these det positions created with a path generator.
    det_pos0 = Detector(name='nai_pos0', position=np.array([45, -32]), material='NaI',
                        detector_number=4, orientation=315, time=0)
    det_pos1 = Detector(name='nai_pos1', position=np.array([15, -20]), material='NaI',
                                        detector_number=4, orientation=315, time=35)
    det_pos2 = Detector(name='nai_pos2', position=np.array([-20, -20]), material='NaI',
                                        detector_number=4, orientation=25, time=35 + 50)
    det_pos3 = Detector(name='nai_pos3', position=np.array([0, 0]), material='NaI',
                                        detector_number=4, orientation=25, time=100)
    det_pos4 = Detector(name='nai_pos4', position=np.array([-40, 40]), material='NaI',
                        detector_number=4, orientation=315, time=22 + 35 + 35 + 30)

    # define environment
    environment = Playground()
    # add items
    # Sources
    environment.add_tracked_item(cs137_1)
    environment.add_tracked_item(cs137_2)

    # Detectors
    environment.add_tracked_item(det_pos0)
    environment.add_tracked_item(det_pos1)
    environment.add_tracked_item(det_pos2)
    environment.add_tracked_item(det_pos3)
    environment.add_tracked_item(det_pos4)
    environment.add_measurement_plan(waypoints=[det_pos0.name, det_pos1.name, det_pos2.name,
                                                det_pos3.name, det_pos4.name],
                                     plan_name='detector_movement',
                                     time_step=1,
                                     sub_time_step=0.2)
    # print(environment.plans['detector_movement'].observed_object_list)
    # print(environment.plans['detector_movement'].physical_object_list)
    # print(len(environment.plans['detector_movement'].observed_object_list))
    # print(len(environment.plans['detector_movement'].physical_object_list))

    fig, ax, art = environment.plotme()
    fig.savefig('test_playground.png', additional_artists=art, bbox_inches='tight')
    return

main()

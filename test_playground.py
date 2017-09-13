
from playground import Playground
from items import Detector, Source
import numpy as np

def main():

    # Define items
    cs137_1 = Source(name='cs137_1', position=np.array([20, 20]), isotope='cs137',
                     activity_mCi=1)
    cs137_2 = Source(name='cs137_2', position=np.array([-25, -35]), isotope='cs137',
                     activity_mCi=0.25)
    # NOTE: Have these det positions created with a path generator.
    det_pos0 = Detector(name='nai_pos0', position=np.array([40, -40]), material='NaI',
                        detector_number=4, orientation=315)
    det_pos1 = Detector(name='nai_pos1', position=np.array([25, -25]), material='NaI',
                        detector_number=4, orientation=315)
    det_pos2 = Detector(name='nai_pos2', position=np.array([0, 0]), material='NaI',
                        detector_number=4, orientation=315)
    det_pos3 = Detector(name='nai_pos3', position=np.array([-25, 25]), material='NaI',
                        detector_number=4, orientation=315)
    det_pos4 = Detector(name='nai_pos4', position=np.array([-40, 40]), material='NaI',
                        detector_number=4, orientation=315)

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

    fig, ax = environment.plot_grid()

    fig.savefig('test_playground.png')
    return

main()

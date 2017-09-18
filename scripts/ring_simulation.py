
import sys
sys.path.append('/home/holiestcow/Documents/2017_fall/ne697_hayward')

from radsynth.core.playground import Playground
from radsynth.core.items import Detector, Source
import numpy as np


def main():

    # Define items
    # Define sources using the ringer
    sources = Source.setup_ring_simulation(radius=10, dphi=1, phi_min=0, phi_max=180,
                                           object_prefix='halfspan')
    # define detector
    detector = Detector(name='nai_pos0', position=np.array([0, 0]), material='NaI',
                        detector_number=20, orientation=0, time=0)

    # define environment
    environment = Playground(width=25, height=25)
    # add items
    for source in sources:
        environment.add_tracked_item(source)
    environment.add_tracked_item(detector)

    fig, ax = environment.plotme(plot_width=12, plot_height=12, legend_position=(1.75, 1),
                                 legend_column_number=4)

    fig.savefig('ring_simulation.png')
    return

main()

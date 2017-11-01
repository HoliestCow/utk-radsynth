
import sys
sys.path.append('/home/holiestcow/Documents/2017_fall/ne697_hayward')

from radsynth.core.playground import Playground
from radsynth.core.items import Detector, Source
import numpy as np


def main():

    environment = Playground(width=25, height=25)

    # Define items
    # Define sources using the ringer
    # sources = Source.setup_ring_simulation(radius=10, dphi=1, phi_min=0, phi_max=180,
    #                                        object_prefix='halfspan')
    # define detector
    # detector = Detector(name='nai_pos0', position=np.array([0, 0]), material='NaI',
    #                     detector_number=20, orientation=0, time=0)

    environment.setup_ring_simulation(radius=10, dphi=1, phi_min=0, phi_max=360,
                                      object_prefix='fullspan')

    # define environment
    # add items
    # for source in sources:
    #     environment.add_tracked_item(source)
    # environment.add_tracked_item(detector)

    fig, ax, art = environment.plotme(plot_width=12, plot_height=12, legend_position=(1.75, 1),
                                      legend_column_number=4)
    fig.savefig('ring_simulation.png',
                additional_artists=art, bbox_inches='tight')

    environment.write_geant_macros(
        output_prefix='/home/cbritt2/ne692_hayward/ddli-code/geant4',
        output_suffix='ringer', local_output='/home/holiestcow/Documents/2017_fall/ne697_hayward/ddli-code/geant4/scripts/ring_batch',
        batch_name='ringer',
        nparticles=10000000,
        macro_type='ring')  # 1e7

    # At this point, what is left is to generate the macros to run in GEANT to get the angular response
    # for source in environment.get_tracked_sources():


    return

main()

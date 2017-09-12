# python 3.6
from data_classes import DetectorArray
from generators import DetectorResponseGenerator

# This is the rough draft for the ultimate calling script.
# This calling script will create an hdf5 file filled with time stamped spectra
# for each detector for a given detector array or system.

def main():
    # System response as a function of source incident angle.
    # This is generated using a ring simulation around the system.
    # This is a function of the source type, fixed source radius, angular resolution.
    angular_response = AngularResponse('ringsim_data.h5')

    # Path response as a function of source position within the environment
    # Function of source type, x, y, system orientation,
    #     spatial resolution (every 100 cm ticks between two positions).
    path_response = PathResponse('pathsim_data.h5')

    # Input parameters
    source_strength = 100  # microCurie
    system_speed_mps = 1  # meters per second
    integration_time_ms = 1000  # millisecond. How long the counting time is for the system
    num_bins = 2**10  # how many bits are in the ADC. How many bins make the spectra.

    # synthetic data consists of a table of data consisting of time stamp, system position
    #       in x and y (cm), and spectra for each detector.
    # This class will synthetically sample at the finer ticks, then aggregate the fine ticks into
    #    the course measurement at the set integration time.
    synthetic_data = DetectorResponseGenerator(
        angular_response=angular_response,
        path_response=path_response,
        source_strength_muCi=source_strength,
        integration_time_ms=integration_time_ms,
        system_speed_mps=system_speed_mps,
        num_bins=num_bins)

    # plot synthetic_data such that other homies can understand what they're looking at.
    plot_synthetic_data(synthetic_data)
    # export synthetic_data so other homies can import and use it.
    HDF5_export(synthetic_data)


def plot_synthetic_data(data):
    pass


def HDF5_export(data):
    pass

main()








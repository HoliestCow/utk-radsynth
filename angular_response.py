
import h5py
import numpy as np
from scipy.interpolate import interp1d


class AngularResponse(object):
    # TODO: object or ABC: Abstract Base Class???

    def __init__(self, h5filepath):
        # Monte Carlo data is just a table for a given system.
        # The name will describe the system
        # The metadata field will describe the information used in generating the results
        #     has to capture the assumptions made on the detection system.
        # angular_response will have row, which contains the spectra for each detector
        #     Each column represents the detector index.
        monte_carlo_data = h5py.File(h5filepath, 'r')
        self.metadata = monte_carlo_data['/meta']
        self.angles = monte_carlo_data['/angles']
        angular_group = monte_carlo_data['/response']
        angular_response = []
        self.detector_names = list(angular_group.keys())
        self.detector_number = len(self.detector_names)
        for detector_index in range(self.detector_number):
            angular_response += [np.array(angular_group[detector_index])]
        # det index, angle, bin_number
        self.angular_response = np.array(angular_response)
        self.angular_response_interpolator = []
        for i in self.angular_response.shape[0]:
            # axis=1 or 0
            self.angular_response_interpolator += [interp1d(
                self.angles, np.squeeze(self.angular_response[i, :, :]), axis=1, kind='linear')]

        return

    def get_response(self, phi):
        # 2d array of interpolated responses.
        # phi, spectra
        desired_value = np.zeros((len(phi), self.detector_number))
        for i in range(self.detector_number):
            desired_value[:, i] = self.angular_response_interpolator[i](phi)
        return desired_value


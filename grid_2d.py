
import numpy as np
from detector import Detector

class Grid2D(object):
    # Playground describes everything going on in the simulation.
    #     Keeps track of everything
    # Center of the grid is [0, 0]
    def __init__(self, width=100, height=100, pixel_width=1, pixel_height=1):
        # All in meters
        leftandright = width/2
        upanddown = height/2
        px_x = np.linspace(-leftandright, leftandright, width/pixel_width)
        px_y = np.linspace(-upanddown, upanddown, height/pixel_height)

        return

    def set_system_path(self, x, y):
        self.x = x
        self.y = y
        return

    def set_source_position(self, x, y):
        pass
        return

    def meter2index(self, x, y):
        pass
        return

    def index2meter(self, x, y):
        pass
        return


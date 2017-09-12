
import numpy as np
from detector import Detector


class Pixel(object):
    def __init__(self, position=None, pixel_width=None):
        self.pixel_width = pixel_width
        self.position_bottom_left = position
        self.position_center = (position[0] + (pixel_width / 2),
                                position[1] + (pixel_width / 2))
        self.items = {}

    def add_item(self, item_name, item):
        # Items are like sources or detector systems.
        self.items[item_name] = item

    def remove_item(self, item):
        # Items are like sources or detector systems.
        if item in self.items:
            del self.items[item]


class Playground(object):
    # Playground describes everything going on in the simulation.
    #     Keeps track of everything
    # Center of the grid is [0, 0]
    def __init__(self, width=100, height=100, pixel_width=1):
        # All in meters
        leftandright = width/2
        upanddown = height/2
        self.pixel_width = pixel_width
        # TODO: Consider pixel objects.
        # TODO: Consider Grid2D to be composed of pixel objects.
        px_i = np.linspace(-leftandright, leftandright, width / pixel_width)
        px_j = np.linspace(-upanddown, upanddown, height / pixel_width)
        # px_coords = np.meshgrid(px_x, px_y)
        # No clue what meshgrid does, so will code this with looperinos
        self.pixels = np.ndarray((len(px_i), len(px_j)), dtype=np.dtype(object))
        for j in range(px_j.size):
            # along the x (j)
            for i in range(px_i.size):
                # along y (i)
                px_coords = (px_i[i], px_j)
                self.pixels[i, j] = Pixel(position=px_coords, pixel_width=self.pixel_width)
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



import sys
sys.path.append('/home/holiestcow/Documents/2017_fall/ne697_hayward')

import numpy as np
import matplotlib.pylab as plt
from radsynth.core.items import Obstacle, Detector
from radsynth.core.pathing import Plan
import matplotlib._color_data as mcd
# from matplotlib import pylab


class Pixel(object):
    def __init__(self, position=None, pixel_width=None):
        self.pixel_width = pixel_width
        position_bottom_left = position
        position_center = np.array([position[0] + (pixel_width / 2),
                                    position[1] + (pixel_width / 2)])
        self.position = {'bottom_left': position_bottom_left,
                         'position_center': position_center}
        self.source_score = 0


class Playground(object):
    # Playground describes everything going on in the simulation.
    #     Keeps track of everything
    # Center of the grid is [0, 0] in meters and [
    # note that the center of the grid is the bottom left of the center pixel
    #     this implies that ownership of pixel is inherited to the top right
    def __init__(self, width=100, height=100, pixel_width=1):
        self.color_wheel = mcd.XKCD_COLORS
        self.color_list = list(mcd.XKCD_COLORS.keys())

        self.items = {}
        self.plans = {}
        self.color_counter = 0

        # All in meters
        self.width = width
        self.height = height
        self.pixel_width = width
        leftandright = width / 2
        upanddown = height / 2
        self.left_offrame = -leftandright
        self.right_offrame = leftandright
        self.bottom_offrame = -upanddown
        self.top_offrame = upanddown
        # TODO: Consider pixel objects.
        px_i = np.linspace(self.left_offrame, self.right_offrame, self.width / pixel_width)
        px_j = np.linspace(-self.bottom_offrame, self.top_offrame, self.height / pixel_width)
        # px_coords = np.meshgrid(px_x, px_y)
        # No clue what meshgrid does, so will code this with looperinos

        self.pixels = np.ndarray((len(px_i), len(px_j)), dtype=np.dtype(object))
        for j in range(px_j.size):
            # along the x (j)
            for i in range(px_i.size):
                # along y (i)
                px_coords = np.array([px_i[i], px_j[j]])
                self.pixels[i, j] = Pixel(position=px_coords, pixel_width=self.pixel_width)
        # True north reference point
        north_pole = Obstacle(name='north_pole', position=np.array([0, self.top_offrame]),
                              speed=0, orientation=0, isVisible=False)
        self.add_tracked_item(north_pole)
        self.north_pole = north_pole

        return

    def add_tracked_item(self, item):
        # item_name is a string
        # item is an Item object
        if item.name in self.items:
            print('Error: {} already present in Playground.\
                   Item was not added nor overwritten.\n Tracked items: {}'.format(item.name,
                                                                                   self.items))
        else:
            # have to define the index position for this playground and assign it.
            index_position = self.meter2index(item.position['meters'])
            item.position['index'] = index_position
            item.color = self.color_wheel[self.color_list[self.color_counter]]
            self.color_counter += 1
            self.items[item.name] = item
        return

    def remove_tracked_item(self, item):
        if item.name in self.items:
            del self.items[item.name]
            self.color_counter -= 1
        else:
            print('Error: Item {} was not found in PlayGround.\
                  No changes were made.\n Tracked items: {}'.format(item.name,
                                                                    self.items))
        return

    def get_tracked_items(self):
        return self.items

    def meter2index(self, position):
        # position should be a np.array of floats
        x, y = position
        pixel_j = int(np.floor(x / self.pixel_width))
        pixel_i = int(np.floor(y / self.pixel_width))
        position = [pixel_i, pixel_j]
        # position in indexes should be a list of int
        return position

    def index2meter(self, position, flavor='BL'):
        i, j = position
        if flavor == 'BL':
            # bottom left of pixel
            x = (j * self.pixel_width) + self.left_offrame
            y = -(i * self.pixel_width) + self.right_offrame
        elif flavor == 'center':
            x = (j * self.pixel_width) + self.left_offrame + (self.pixel_width / 2)
            y = -(i * self.pixel_width) + self.right_offrame + (self.pixel_width / 2)
        else:
            raise ValueError('flavor {} is not included in index2meter'.format(flavor))
        # should be np array of floats
        position = np.array([x, y])
        return position

    def distance_between(self, object1_name, object2_name):
        if object1_name not in self.items:
            raise ValueError('Error: Object {} not tracked within Playground'.format(object1_name))
        elif object2_name not in self.items:
            raise ValueError('Error: Object {} not tracked within Playground'.format(object2_name))
        object1 = self.items[object1_name]
        object2 = self.items[object2_name]
        pos_object1 = object1.position['meters']
        pos_object2 = object2.position['meters']
        distance = np.linalg.norm(pos_object1 - pos_object2)
        return distance

    def angle_between(self, object1_name, object2_name):
        # Angle of object2 relative to object1
        if object1_name not in self.items:
            raise ValueError('Error: Object {} not tracked within Playground'.format(object1_name))
        elif object2_name not in self.items:
            raise ValueError('Error: Object {} not tracked within Playground'.format(object2_name))
        object1 = self.items[object1_name]
        object2 = self.items[object2_name]
        pos_object1 = object1.position['meters']
        pos_object2 = object2.position['meters']
        dpos = pos_object2 - pos_object1
        anglefromnorth = (np.rad2deg(np.arctan(dpos[0] / dpos[1])))
        # if relative_angle < 0:
        #     relative_angle += 360
        # elif relative_angle > 360:
        #     relative_angel -= 360
        # v1_u = self.unit_vector(pos_object1)
        # v2_u = self.unit_vector(pos_object2)
        # print(self.unit_vector(dpos))
        # TODO: Check to make sure this is the relative angle from Object1's perspective.
        # object 1 will usually be the detector.
        return anglefromnorth

    def unit_vector(self, vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    def plotme(self, plot_height=6, plot_width=8,
               legend_position=(1.5, 1), legend_column_number=1):
        fig, ax = plt.subplots()
        fig.set_size_inches(plot_width, plot_height)
        # make a little more margin
        ax.set_xlim(self.left_offrame, self.right_offrame)
        ax.set_ylim(self.bottom_offrame, self.top_offrame)
        for key in self.plans:
            plan = self.plans[key]
            # for i in range(len(plan.segments)):
            #     segment = plan.segments[i]
            #     color = segment['color']
            #     coords = segment['position']
            #     ax.plot(coords[:, 0], coords[:, 1], '.', c=color, markersize=1)
            for detector in plan.get_refined_object_list():
                ax.scatter(detector.position['meters'][0], detector.position['meters'][1],
                           c=detector.color, s=4)
                phi = detector.orientation
                dx = np.sin(np.deg2rad(phi))
                dy = np.cos(np.deg2rad(phi))
                ax.arrow(detector.position['meters'][0], detector.position['meters'][1],
                         dx, dy, color='k', lw=0.2)
        for key in self.items:
            individual = self.items[key]
            if type(individual) is Obstacle:
                if individual.isVisible is False:
                    continue
            coords = individual.position['meters']
            ax.plot(coords[0], coords[1], individual.marker, c=individual.color,
                    label=individual.name)
            # if type(individual) is Detector:
            #     phi = individual.orientation
            #     dx = 5 * np.sin(np.deg2rad(phi))
            #     dy = 5 * np.cos(np.deg2rad(phi))
            #     ax.arrow(coords[0], coords[1], dx, dy, color='k')
        # for key in self.items:
        #     individual = self.items[key]
        #     coords = individual.position['meters']
        #     if type(individual) is Detector:
        #         # TODO: Don't know why this isn't working :/
        #         phi = individual.orientation
        #         dx = 5 * np.sin(np.deg2rad(phi))
        #         dy = 5 * np.cos(np.deg2rad(phi))
        #         ax.arrow(coords[0], coords[1], dx, dy, color='k')
        ax.set_xlabel('x_position (m)')
        ax.set_ylabel('y_position (m)')
        # ax.legend(bbox_to_anchor=(1, 1), loc='upper right', ncol=1)
        art = []
        lgd = plt.legend(loc=9, bbox_to_anchor=legend_position, ncol=legend_column_number)
        art.append(lgd)
        plt.savefig(
            'test.png', additional_artists=art,
            bbox_inches='tight')
        return fig, ax

    def add_measurement_plan(self, waypoints=[], plan_name=None, time_step=0.2):
        object_list = []
        for i in range(len(waypoints)):
            object_list += [self.items[waypoints[i]]]
        self.plans[plan_name] = Plan(object_list, time_step)

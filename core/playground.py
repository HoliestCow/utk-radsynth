
import sys
sys.path.append('/home/holiestcow/Documents/2017_fall/ne697_hayward')

import numpy as np
import matplotlib.pylab as plt
from radsynth.core.items import Obstacle, Detector, Source
from radsynth.core.pathing import Plan
import matplotlib._color_data as mcd
import os.path
import textwrap
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

    def get_tracked_objects(self, object_type=None):
        if object_type is None:
            return self.items
        out = []
        for item in self.items:
            if isinstance(self.items[item], object_type):
                out += [self.items[item]]
        return out

    # def get_tracked_items(self):
    #     return self.items
    #
    # def get_tracked_sources(self):
    #     stuff = self.get_tracked_items()
    #     out = []
    #     for item in stuff:
    #         if isinstance(self.items[item], Source):
    #             out += [self.items[item]]
    #     return out
    #
    # def get_tracked_detectors(self):
    #     stuff = self.get_tracked_items()
    #     out = []
    #     for item in stuff:
    #         if isinstance(self.items[item], Detector):
    #             out += [self.items[item]]
    #     return out
    #
    # def get_tracked_plans(self):
    #     stuff = self.get_tracked_items()
    #     out = []
    #     for item in stuff:
    #         if isinstance(self.items[item], Plan):
    #             out += [self.items[item]]
    # return out

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
        if isinstance(object1_name, str) and isinstance(object2_name, str):
            if object1_name not in self.items:
                raise ValueError('Error: Object {} not tracked within Playground'.format(object1_name))
            elif object2_name not in self.items:
                raise ValueError('Error: Object {} not tracked within Playground'.format(object2_name))
            object1 = self.items[object1_name]
            object2 = self.items[object2_name]
        # else:
        #     object1 = object1_name
        #     object2 = object2_name
        pos_object1 = object1.position['meters']
        pos_object2 = object2.position['meters']
        distance = np.linalg.norm(pos_object1 - pos_object2)
        return distance

    def angle_between(self, object1_name, object2_name):
        # Angle of object2 relative to object1
        if isinstance(object1_name, str) and isinstance(object2_name, str):
            if object1_name not in self.items:
                raise ValueError('Error: Object {} not tracked within Playground'.format(object1_name.name))
            elif object2_name not in self.items:
                raise ValueError('Error: Object {} not tracked within Playground'.format(object2_name.name))
            object1 = self.items[object1_name]
            object2 = self.items[object2_name]
        # else:
        #     object1 = object1_name
        #     object2 = object2_name
        pos_object1 = object1.position['meters']
        pos_object2 = object2.position['meters']
        dpos = pos_object2 - pos_object1
        angle = np.rad2deg(np.arctan(dpos[1] / dpos[0]))
        if dpos[0] >= 0 and dpos[1] >= 0:
            angle = 90 - angle
        elif dpos[0] <= 0 and dpos[1] <= 0:
            angle = 270 - angle
        elif dpos[0] >= 0 and dpos[1] <= 0:
            angle = 90 - angle
        elif dpos[0] <= 0 and dpos[1] >= 0:
            angle = 270 - angle
        return angle

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
            for detector in plan.physical_object_list:
                ax.scatter(detector.position['meters'][0], detector.position['meters'][1],
                           c=detector.color, s=1)
                phi = detector.orientation
                dx = np.sin(np.deg2rad(phi))
                dy = np.cos(np.deg2rad(phi))
                ax.arrow(detector.position['meters'][0], detector.position['meters'][1],
                         dx, dy, color='k', lw=0.2)
            for detector in plan.observed_object_list:
                ax.scatter(detector.position['meters'][0], detector.position['meters'][1],
                           c=detector.color, s=4)
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
        for detector in self.get_tracked_objects(object_type=Detector):
            for source in self.get_tracked_objects(object_type=Source):
                phi = self.angle_between(detector.name, source.name)
                dx = 5 * np.sin(np.deg2rad(phi))
                dy = 5 * np.cos(np.deg2rad(phi))
                ax.arrow(detector.position['meters'][0], detector.position['meters'][1], dx, dy, color='k')
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
        # plt.savefig(
        #     'test.png', additional_artists=art,
        #     bbox_inches='tight')
        return fig, ax, art

    def add_measurement_plan(self, waypoints=[], plan_name=None,
                             time_step=1, sub_time_step=0.2):
        object_list = []
        for i in range(len(waypoints)):
            object_list += [self.items[waypoints[i]]]
        self.plans[plan_name] = Plan(name=plan_name, listofobjects=object_list, time_step=time_step, sub_time_step=sub_time_step)

        for detector in self.plans[plan_name].physical_object_list:
            self.add_tracked_item(detector)
        return

    def setup_ring_simulation(self, radius=10, dphi=1, phi_min=0, phi_max=360,
                              object_prefix='fullspan', isotope='cs137'):
        # radius in meters, phi in degrees.
        phi = np.arange(phi_min, phi_max + 0.01, dphi)
        # setup source at the center of the circle
        source = Source(name='{}_center'.format(isotope), position=np.array([0., 0.]),
                        isotope=isotope, activity_mCi=100.)
        self.add_tracked_item(source)
        for i in range(len(phi)):
            object_label = '{}_{}_angle{}_radius{}'.format(object_prefix, i, phi[i], radius)
            x_position = radius * np.sin(np.deg2rad(phi[i]))
            y_position = radius * np.cos(np.deg2rad(phi[i]))
            position = np.array([x_position, y_position])
            detector_object = Detector(name=object_label, position=position, material='NaI',
                                       orientation=phi[i] + 180.)
            self.add_tracked_item(detector_object)
        return

    def angle_between_2geant4(self, object1_name, object2_name):
        return 90.0 - self.angle_between(object1_name, object2_name)

    def write_geant_macros(self, output_prefix, batch_name, local_output='./',
                           output_suffix=None, nparticles=10000, macro_type='plan'):
        # plans = self.get_tracked_objects(object_type=Plan)
        if macro_type == 'plan':
            # HACK: Assume single plan. quickly extract then loop.
            stuff = self.plans.keys()
            playlist = self.plans[list(stuff)[0]].physical_object_list
        elif macro_type == 'ring':
            playlist = self.get_tracked_objects(object_type=Detector)
        counter = 1
        double_counter = 1
        batch_f = open(os.path.join(local_output, batch_name+'.sh'), 'w')
        batch_f.write('#!/bin/bash\n\n')
        print(len(playlist))
        for detector in playlist:
            # For ring I'm already in detector level
            # For plan I'm in the plan level
            # for detector in item.physical_object_list:
            filename = os.path.join(output_prefix, batch_name + '_' + detector.name)
            if output_suffix:
                # filename = os.path.join(filename, output_suffix, '.mac')
                filename = '{}_{}.mac'.format(filename, output_suffix)
            else:
                # filename = os.path.join(filename, '.mac')
                filename = '{}.mac'.format(filename)
            head, tail = os.path.split(filename)

            # WRITE THE DDLISIM FILE
            local_filename = os.path.join(local_output, tail)
            print(local_filename)
            single_f = open(local_filename, 'w')
            single_f.write('\n')
            for source in self.get_tracked_objects(object_type=Source):
                single_f.write('/ddli/run/out_path {}.root\n'.format(filename[:-4]))
                single_f.write('/ddli/gun/distance {} m\n'.format(
                    self.distance_between(detector.name, source.name)))
                # I have to convert from my coordinate system to GEANT4
                single_f.write('/ddli/gun/angle {} degree\n'.format(
                    self.angle_between_2geant4(detector.name, source.name)))
                single_f.write('/ddli/geometry/reload\n')
                single_f.write('/run/beamOn {}\n\n'.format(nparticles))
            single_f.close()


            '''
            #!/bin/bash

            #PBS -N testeroony
            #PBS -l walltime=24:00:00
            #PBS -t 1-610
            #PBS -l nodes=1:ppn=4
            #PBS -q gen2

            /home/cbritt2/ne692_hayward/ddli-code/geant4/${PBS_ARRAYID}.sh
            '''
            # IF MODULO == 0, THEN CLOSE THE GROUP_F, start a new one,
            #    add to the qsub submission bash script
            # WRITE THE DDLISIM BATCHER THAT SHOULD BE IN PARALLEL. ON A PER NODE BASIS
            if counter == 1:
                array_filename = '{}.sh'.format(double_counter)
                array_filename = os.path.join(local_output, array_filename)
                group_f = open(array_filename, 'w')
                group_f.write('#!/bin/bash\n')
                group_f.write('#PBS -N testeroony_{}\n'.format(double_counter))
                group_f.write('#PBS -l walltime=06:00:00\n#PBS -l nodes=1:ppn=4\n#PBS -q gen2\n\n')
                group_f.write('cd {}\n\n'.format(output_prefix))

            if counter % 4 == 0:
                group_f.write('wait\n')
                group_f.close()
                batch_f.write('qsub {}.sh\n'.format(double_counter))
                array_filename = '{}.sh'.format(double_counter)
                array_filename = os.path.join(local_output, array_filename)
                group_f = open(array_filename, 'w')
                group_f.write('#!/bin/bash\n')
                group_f.write('#PBS -N testeroony_{}\n'.format(double_counter))
                group_f.write('#PBS -l walltime=06:00:00\n#PBS -l nodes=1:ppn=4\n#PBS -q gen2\n\n')
                group_f.write('cd {}\n\n'.format(output_prefix))
                double_counter += 1

            # ADD TO THE BATCH FILE
            group_f.write('{}/DDLISim {} & \n'.format(output_prefix, filename))
            counter += 1
        if counter % 4 != 0:
            group_f.write('wait \n')
            group_f.close()
        batch_f.close()


# #!/bin/bash
#
# #PBS -N echotesting
# #PBS -l walltime=00:05:00
# #PBS -l nodes=1:ppn=2
# #PBS -t 1-4%2
# #PBS -q gen1
#
# cd /home/cbritt2/ne692_hayward
# ./${PBS_ARRAYID}.sh
# """))

        return

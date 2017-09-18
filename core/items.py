import numpy as np


class Item(object):

    def __init__(self, name=None, position=None, orientation=0, speed=0, marker=None, color=None):
        self.name = name
        self.position = {'meters': position, 'index': None}
        self.speed = speed
        self.orientation = orientation
        self.marker = marker
        self.color = color
        return


class Obstacle(Item):
    def __init__(self, name=None, position=None, speed=0, orientation=0, marker='+',
                 isVisible=True):
        super().__init__(name=name, position=position, orientation=orientation,
                         speed=speed, marker=marker)
        self.isVisible = isVisible
        return


class Source(Item):

    def __init__(self, name=None, position=None, isotope=None, activity_mCi=None,
                 orientation=0, speed=0, isIsotropic=True):
        super().__init__(name=name, position=position,
                         orientation=orientation, speed=speed, marker='x')
        self.isotope = isotope
        self.activity_mCi = activity_mCi
        self.orientation = orientation
        self.speed = 0
        self.isIsotropic = isIsotropic
        return

    @staticmethod
    def setup_ring_simulation(radius=10, dphi=1, phi_min=0, phi_max=360, object_prefix='source',
                              isotope='cs137'):
        # radius in meters, phi in degrees.
        phi = np.arange(phi_min, phi_max + 0.01, dphi)
        objects = []
        for i in range(len(phi)):
            object_label = '{}_{}_angle{}_radius{}'.format(object_prefix, i, phi[i], radius)
            x_position = radius * np.sin(np.deg2rad(phi[i]))
            y_position = radius * np.cos(np.deg2rad(phi[i]))
            position = np.array([x_position, y_position])
            source_object = Source(name=object_label, position=position, isotope=isotope)
            objects += [source_object]
        return objects


class Detector(Item):
    def __init__(self, name=None, position=None, material=None, detector_number=1,
                 orientation=0, speed=0, time=None):
        super().__init__(name=name, position=position,
                         orientation=orientation, speed=speed, marker='o')
        self.material = material
        self.detector_number = detector_number
        self.orientation = orientation
        self.time = time
        return

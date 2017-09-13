

class Item(object):

    def __init__(self, name=None, position=None, orientation=0, speed=0, marker=None):
        self.name = name
        self.position = {'meters': position, 'index': None}
        self.speed = speed
        self.orientation = orientation
        self.marker = marker
        return


class Obstacle(Item):
    def __init__(self, name=None, position=None, speed=0, orientation=0, marker='+', isVisible=True):
        super().__init__(name=name, position=position, orientation=orientation,
                         speed=speed, marker=marker)
        self.isVisible = isVisible
        return


class Source(Item):

    def __init__(self, name=None, position=None, isotope=None, activity_mCi=None,
                 orientation=0, speed=0):
        super().__init__(name=name, position=position,
                         orientation=orientation, speed=speed, marker='x')
        self.isotope = isotope
        self.activity_mCi = activity_mCi
        self.orientation = orientation
        self.speed = 0
        return


class Detector(Item):
    def __init__(self, name=None, position=None, material=None, detector_number=1,
                 orientation=0, speed=0):
        super().__init__(name=name, position=position,
                         orientation=orientation, speed=speed, marker='o')
        self.material = material
        self.detector_number = detector_number
        self.orientation = orientation
        return

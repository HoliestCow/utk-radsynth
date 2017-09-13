

class Item(object):

    def __init__(self, name=None, position=None, isStatic=True, orientation=0):
        self.name = name
        self.position = {'meters': position, 'index': None}
        self.isStatic = isStatic
        self.orientation = orientation
        return


class Source(Item):

    def __init__(self, name=None, position=None, isotope=None, activity_mCi=None, isStatic=True,
                 isIsotropic=True, orientation=0):
        super().__init__(**kwargs)
        self.isotope = isotope
        self.activity_mCi = activity_mCi
        self.orientation = orientation
        self.isIsotropic = isIsotropic
        self.marker = 'x'
        return


class Detector(Item):
    def __init__(self, name, position=None, material=None, detector_number=1, isStatic=True,
                 orientation=0):
        super().__init__(position=position)
        self.material = material
        self.detector_number = detector_number
        self.isStatic = isStatic
        self.orientation = orientation
        self.marker=
        return

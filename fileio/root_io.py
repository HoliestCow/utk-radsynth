import rootpy.io
import root_numpy

class GeantImport(object):
    def __init__(self):
        return
    def get_tree(self, filename):
        ROOT.gInterpreter.Declare(
            '#include "/home/holiestcow/Documents/2017_fall/ne697_hayward/ddli-code/geant4/include/detevent.hpp"')
        f = rootpy.io.File(filename, 'READ')
        return test
import sys
sys.path.append('/home/holiestcow/Documents/2017_fall/ne697_hayward')

# import ROOT
# import numpy as np
from radsynth.fileio.root_io import GeantImport
import matplotlib.pyplot as plt


def main():
    datgeant4path = '/home/holiestcow/Documents/2017_fall/ne697_hayward/ddli-code/geant4/'
    desired_path = '{}lib/libddli-sim'.format(datgeant4path)

    rootio = GeantImport(desired_path)
    x, y, y_norm = rootio.get_spectra('../../ddli-code/geant4/output/trailer_test.root',
                                      bits=10, detectorID=None)
    fig = plt.figure()
    plt.plot(x, y)
    plt.xlabel('Energy')
    plt.ylabel('Frequency')
    fig.savefig('rootioclass_test.png')
    plt.close(fig)

    fig = plt.figure()
    plt.plot(x, y_norm)
    plt.xlabel('Energy')
    plt.ylabel('Normalized Frequency')
    fig.savefig('rootioclass_normalized_test.png')
    plt.close(fig)
    return

main()
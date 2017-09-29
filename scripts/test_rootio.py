import sys
sys.path.append('/home/holiestcow/Documents/2017_fall/ne697_hayward')

import ROOT
import numpy as np
import matplotlib.pyplot as plt

def main():
    datgeant4path = '/home/holiestcow/Documents/2017_fall/ne697_hayward/ddli-code/geant4/'
    #######
    # This is to import the library file generated from compiling ddli-sim geant 4 sim.
    # This is a .so file.
    # This is basically importing the DetEvent class from geant4/src/detevent.cpp
    desired_path = '{}lib/libddli-sim'.format(datgeant4path)
    ROOT.gSystem.Load(desired_path)
    #######

    # Open root file and give it a file handle
    f = ROOT.TFile.Open('test.root')
    # Extract the tree from the file. This assumes the tree name is "Events"
    tree = f.Events

    # intialize storage containers for plotting later.
    energy_storage = []

    # Loop through each event history
    for i in range(tree.GetEntries()):
        # YOU HAVE TO DO THIS. This is because under the hood, the histograms seen in TBrowser() are comprised of many DetEvent objects.
        tree.GetEntry(i)
        # Not sure what this is to be honest.
        ed = tree.event
        # YOU NOW HAVE ACCESS TO ALL OF DETEVENT METHODS DEFINED IN geant4/src/detevent.cpp
        # print(ed.getEnergy())
        energy_storage += [ed.getEnergy()]

    # Data is now imported, manipulate at will my homies.
    energy = np.array(energy_storage)
    n, bins, patches = plt.hist(energy, 1024)
    fig = plt.figure()
    # I have to replot. The first bin is the garbage bin where all the particle deaths get lumped in. I think. This is fixed if you supply a cutoff energy and throw away the information instead of logging it in the file.
    plt.bar(bins[2:], n[1:])

    plt.xlabel('Energy')
    plt.ylabel('Frequency')
    # plt.axis([0, max(bins), 0, max(n)])
    plt.title('I would like to thank my mom and dad')
    fig.savefig('rootio_test.png')
    return

main()
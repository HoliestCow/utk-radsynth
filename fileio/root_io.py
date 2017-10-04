import sys
sys.path.append('/home/holiestcow/Documents/2017_fall/ne697_hayward')

import ROOT
import numpy as np
# import matplotlib.pyplot as plt


class GeantImport(object):

    def __init__(self, sharedobject_path):
        ROOT.gSystem.Load(sharedobject_path)
        return

    def get_spectra(self, filename, bits=10, detectorID=None):
        # detectorID is either None or a list of integers.
        f = ROOT.TFile.Open(filename, 'READ')
        tree = f.Events
        energy_storage = []
        for i in range(tree.GetEntries()):
            tree.GetEntry(i)
            ed = tree.event
            if detectorID is None:
                energy_storage += [ed.getEnergy()]
            else:
                for x in detectorID:
                    if x == ed.getDetectorID():
                        energy_storage += [ed.getEnergy()]
        energy = np.array(energy_storage)
        counts, bins = np.histogram(energy, (2**bits) + 1)
        counts = counts[1:]  # exclude the first bin
        bins = bins[2:]  # exclude first bin and the extra. These are just the bin endpoints
        normalized_counts = np.divide(counts, np.sum(counts))
        return bins, counts, normalized_counts

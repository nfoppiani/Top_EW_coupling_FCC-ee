from ROOT import TFile, TH2D
import glob
from numpy import sqrt

# creates the histograms
hElectron = TH2D("electronEnergyAndAngleHisto", "W-decay electrons energy and cosine of polar angle", 40, 0., 200., 30, -1., 1.)
hElectronReduced = TH2D("electronReducedEnergyAndAngleHisto", "W-decay electrons reduced energy and cosine of polar angle", 40, 0., 1.4, 30, -1., 1.)


file = TFile('theoreticalHistos.root',"READ")
tree = file.Get("MyLCTuple")

for event in tree:




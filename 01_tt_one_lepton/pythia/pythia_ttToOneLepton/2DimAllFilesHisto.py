# this program reads the ntuple.root files contained in the present directory and saves a 'allFilesHisto.root' with the two dimensional histograms of the energy/cosTheta of the electrons whose parent is a W, and the same for the muons
# it is assumed that the beam axis is z; theta is the polar angle

from ROOT import TFile, TH2D
import glob
from numpy import sqrt

# creates the histograms
hElectron = TH2D("electronEnergyAndAngleHisto", "ElectronEnergyAndAngle", 40, 0., 200., 30, -1., 1.)
hMuon = TH2D("muonEnergyAndAngleHisto", "MuonEnergyAndAngle", 40, 0., 200., 30, -1., 1.)

# records the *ntuple.root files list of the present directory
fileList = glob.glob('./*ntuple.root')

for fileName in fileList:
    # reads the ntuple.root file
    file = TFile(fileName,"READ")
    tree = file.Get("MyLCTuple")
    
    # loops over the 99 events of the tree
    for event in tree:
        i = 0      # identifies a particle of the event, varies from 1 to numberOfParticles
        
        # fills the histograms
        for pdgId in tree.mcpdg:

            if pdgId == 11 or pdgId == -11:
                parent0 = tree.mcpa0[i]     # defines the first electron parent
                if parent0 > -1:            # parent0 == -1 if electron has not parents
                    if abs(tree.mcpdg[parent0]) == 24:      # if the electron comes from a W decay
                        energy = tree.mcene[i]
                        px = tree.mcmox[i]
                        py = tree.mcmoy[i]
                        pz = tree.mcmoz[i]
                        cosTheta = pz/sqrt(px**2+py**2+pz**2)
                        hElectron.Fill(energy, cosTheta)
                parent1 = tree.mcpa1[i]     # defines the second electron parent
                if parent1 > -1:
                    if abs(tree.mcpdg[parent1]) == 24:
                        energy = tree.mcene[i]
                        px = tree.mcmox[i]
                        py = tree.mcmoy[i]
                        pz = tree.mcmoz[i]
                        cosTheta = pz/sqrt(px**2+py**2+pz**2)
                        hElectron.Fill(energy, cosTheta)
        
            if pdgId == 13 or pdgId == -13:
                parent0 = tree.mcpa0[i]
                if parent0 > -1:
                    if abs(tree.mcpdg[parent0]) == 24:
                        energy = tree.mcene[i]
                        px = tree.mcmox[i]
                        py = tree.mcmoy[i]
                        pz = tree.mcmoz[i]
                        cosTheta = pz/sqrt(px**2+py**2+pz**2)
                        hMuon.Fill(energy, cosTheta)
                parent1 = tree.mcpa1[i]
                if parent1 > -1:
                    if abs(tree.mcpdg[parent1]) == 24:
                        energy = tree.mcene[i]
                        px = tree.mcmox[i]
                        py = tree.mcmoy[i]
                        pz = tree.mcmoz[i]
                        cosTheta = pz/sqrt(px**2+py**2+pz**2)
                        hMuon.Fill(energy, cosTheta)
    
            i = i+1

    file.Close()

# saves the histograms in 2DimAllFilesHisto.root
savingFile = TFile("./2DimAllFilesHisto.root", "CREATE")
hElectron.Write()
hMuon.Write()
savingFile.Close()
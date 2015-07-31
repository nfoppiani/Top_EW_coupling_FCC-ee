# this program reads the ntuple.root files contained in the present directory and saves a 'allFilesHisto.root' file with the histograms of:
# pdg identification number of the particles of the simulated events (MonteCarlo ones, not the ReConstructed ones)
# the energy of electrons
# the same for the muons
# the energy of the electrons whose parent is a W
# the same for the muons
# the reduced energy 'xf' of the electrons whose parent is a W
# the same for the muons
# the mass of the W that decay in an electron or a muon

# NB for the reduced energy definition see lines 17 to 25

from ROOT import TFile, TH1D
import glob
from numpy import sqrt

# reduced energy definition
top = 173.2         # top mass
w = 80.39           # w boson mass
s = 365**2          # center of mass squared energy

beta = sqrt(1-4*top**2/s)               # beta=v/c of the top
r = w**2/top**2
red = 2/top*sqrt((1-beta)/(1+beta))     # reduction factor: REDUCED ENERGY = xf = energy*red
xfMin = r*(1-beta)/(1+beta)             # minimum xf value (maximum is 1)

print 'beta = ', beta
print 'red = ', red
print 'xfMax = 1'
print 'xfMin = ', xfMin


# creates the histograms
hPdgID = TH1D("pdgIDHisto", "Particles identification code", 12001, -6000., 6000.)
hElectronEnergy = TH1D("electronEnergyHisto", "Electrons energy", 80, 0., 200.)
hMuonEnergy = TH1D("muonEnergyHisto", "Muons energy", 80, 0., 200.)
hElectronPar = TH1D("WElectronHisto", "W-decay electrons energy", 80, 0., 200.)
hMuonPar = TH1D("WMuonHisto", "W-decay muons energy", 80, 0., 200.)
hElectronXf = TH1D("WElectronReducedHisto", "W-decay electrons reduced energy", 80, 0., 1.)
hMuonXf = TH1D("WMuonReducedHisto", "W-decay muons reduced energy", 80, 0., 1.)
hW = TH1D("WMassHisto", "W mass", 80, 0., 200.)

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
            hPdgID.Fill(pdgId)

            if pdgId == 11 or pdgId == -11:
                hElectronEnergy.Fill(tree.mcene[i])
                parent0 = tree.mcpa0[i]     # defines the first electron parent
                if parent0 > -1:            # parent0 == -1 if electron has not parents
                    if abs(tree.mcpdg[parent0]) == 24:      # if the electron comes from a W decay
                        hElectronPar.Fill(tree.mcene[i])
                        hElectronXf.Fill(tree.mcene[i]*red)
                        hW.Fill(tree.mcmas[parent0])
                parent1 = tree.mcpa1[i]     # defines the second electron parent
                if parent1 > -1:
                    if abs(tree.mcpdg[parent1]) == 24:
                        hElectronPar.Fill(tree.mcene[i])
                        hElectronXf.Fill(tree.mcene[i]*red)
                        hW.Fill(tree.mcmas[parent1])
                            
            if pdgId == 13 or pdgId == -13:
                hMuonEnergy.Fill(tree.mcene[i])
                parent0 = tree.mcpa0[i]
                if parent0 > -1:
                    if abs(tree.mcpdg[parent0]) == 24:
                        hMuonPar.Fill(tree.mcene[i])
                        hMuonXf.Fill(tree.mcene[i]*red)
                        hW.Fill(tree.mcmas[parent0])
                parent1 = tree.mcpa1[i]
                if parent1 > -1:
                    if abs(tree.mcpdg[parent1]) == 24:
                        hMuonPar.Fill(tree.mcene[i])
                        hMuonXf.Fill(tree.mcene[i]*red)
                        hW.Fill(tree.mcmas[parent1])
            
            i = i+1

    file.Close()

# creates allFilesHisto.root in the current directory
savingFile = TFile("./allFilesHisto.root", "CREATE")
# saves the histograms in allFilesHisto.root
hPdgID.Write()
hElectronEnergy.Write()
hMuonEnergy.Write()
hElectronPar.Write()
hMuonPar.Write()
hElectronXf.Write()
hMuonXf.Write()
hW.Write()
savingFile.Close()
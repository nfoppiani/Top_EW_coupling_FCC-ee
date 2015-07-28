# this program reads a ntuple.root file and saves a file with the histograms of the pdg identification number of the particles of the simulated (MonteCarlo=mc) event, and the energy of electrons and muons

from ROOT import TFile, TH1D

# reads the rr_rec_5485_1_ntuple.root file
file = TFile("tt_rec_5485_1_ntuple.root","READ")
tree = file.Get("MyLCTuple")

# creates the histograms
hPdgID = TH1D("pdgIDHistogram", "ParticlesID", 4000, -1000., 3000.)
hElectronEnergy = TH1D("electronEnergyHisto", "ElectronEnergy", 20, 0., 180.)
hMuonEnergy = TH1D("muonEnergyHistogram", "MuonEnergy", 20, 0., 180.)

# fills the histograms
for event in tree:
    i = 0
    for pdgId in tree.mcpdg:
        hPdgID.Fill(pdgId)
        if pdgId == 11 or pdgId == -11:
            hElectronEnergy.Fill(tree.mcene[i])
        if pdgId == 13 or pdgId == -13:
            hMuonEnergy.Fill(tree.mcene[i])
        i = i +1

# creates oneFileHisto.root file in the current directory
savingFile = TFile("./oneFileHisto.root", "CREATE")

# saves the histograms in firstHisto.root
hPdgID.Write()
hElectronEnergy.Write()
hMuonEnergy.Write()

file.Close()
savingFile.Close()
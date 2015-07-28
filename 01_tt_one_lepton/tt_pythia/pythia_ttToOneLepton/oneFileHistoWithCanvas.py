# reads a ntuple.root file and saves a file with the histograms of the pdg identification number of the particles of the simulated (MonteCarlo=mc) event, and the energy of electrons and muons
# 'h' stays for histograms in variable names, 'c' for canvas

from ROOT import TFile, TCanvas, TH1D

# reads the ntuple.root file
file = TFile("tt_rec_5485_1_ntuple.root","READ")
tree = file.Get("MyLCTuple")

# creates the histograms
hPdgID = TH1D("pdgIDHistogram", "ParticlesID", 3000, -3000., 3000.)
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

# creates the canvas
cPdgID = TCanvas("ParticlesID", "", 800, 800)
cElectronEnergy = TCanvas("electronEnergy", "", 800, 800)
cMuonEnergy = TCanvas("muonEnergy", "", 800, 800)

# fills the canvas
cPdgID.cd()
hPdgID.Draw()

cElectronEnergy.cd()
hElectronEnergy.Draw()

cMuonEnergy.cd()
hMuonEnergy.Draw()

# saves them in firstHisto.root
savingFile = TFile("./oneFileHistoWithCanvas.root", "CREATE")

cPdgID.Write()
cElectronEnergy.Write()
cMuonEnergy.Write()

file.Close()
savingFile.Close()
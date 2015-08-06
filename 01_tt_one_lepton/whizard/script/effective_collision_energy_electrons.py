from ROOT import TFile, TCanvas, TH1F

#binning of 200 MeV

h_el = TH1F("Effective collision energy with an electron/positron in the final state","Effective collision energy with an electron/positron in the final state",100,345.,365.)

h_leptons = TH1F("Effective collision energy with a heavy lepton in the final state","Effective collision energy with a heavy lepton in the final state",100,345.,365.)

#electron-positron

electrons_file = TFile("../ntuple/electrons_tree.root", "OPEN")
electrons_tree=electrons_file.Get("electrons_tree")

for event in electrons_tree:
	h_el.Fill(electrons_tree.mcInvMas)
	
electrons_file.Close()	

positrons_file = TFile("../ntuple/positrons_tree.root", "OPEN")
positrons_tree=positrons_file.Get("positrons_tree")

for event in positrons_tree:
	h_el.Fill(positrons_tree.mcInvMas)

positrons_file.Close()

c_el = TCanvas("Effective collision energy with an electron/positron in the final state","Effective collision energy with an electron/positron in the final state",800,800)
c_el.cd()
h_el.Draw()

#muons-tau

#positive
positive_muons_file = TFile("../ntuple/positive_muons_tree.root", "OPEN")
positive_muons_tree=positive_muons_file.Get("positive_muons_tree")

for event in positive_muons_tree:
	h_leptons.Fill(positive_muons_tree.mcInvMas)
	
positive_muons_file.Close()	

positive_tau_file = TFile("../ntuple/positive_tau_tree.root", "OPEN")
positive_tau_tree=positive_tau_file.Get("positive_tau_tree")

for event in positive_tau_tree:
	h_leptons.Fill(positive_tau_tree.mcInvMas)

positive_tau_file.Close()

#negative
negative_muons_file = TFile("../ntuple/negative_muons_tree.root", "OPEN")
negative_muons_tree=negative_muons_file.Get("negative_muons_tree")

for event in negative_muons_tree:
	h_leptons.Fill(negative_muons_tree.mcInvMas)
	
negative_muons_file.Close()	

negative_tau_file = TFile("../ntuple/negative_tau_tree.root", "OPEN")
negative_tau_tree=negative_tau_file.Get("negative_tau_tree")

for event in negative_tau_tree:
	h_leptons.Fill(negative_tau_tree.mcInvMas)

negative_tau_file.Close()



c_leptons = TCanvas("Effective collision energy with a heavy lepton in the final state","Effective collision energy with a heavy lepton in the final state",800,800)
c_leptons.cd()
h_leptons.Draw()

from ROOT import TFile, TCanvas, TH1F, TH2F, TTree, TChain
import numpy

tree = TChain("MyLCTuple")
tree.Add("../ntuple/prova/yyxyev_o_*.root")

h_el=TH2F("Energy-angle of reconstructed electrons","Energy-angle of reconstructed electrons",100,0.,120.,10000,-1.,1.)
h_angle=TH1F("angle","angle",10000,-1.,1.)

for event in tree:
	ip=0
	for pdgid in tree.rctyp:
		if pdgid ==11:
			if tree.rcene[ip]>10 and tree.rcene[ip]<120:
				h_el.Fill(tree.rcene[ip],tree.rcmoz[ip]/tree.rcene[ip])
				h_angle.Fill(tree.rcmoz[ip]/tree.rcene[ip])
		ip = ip +1

h_angle.Draw()

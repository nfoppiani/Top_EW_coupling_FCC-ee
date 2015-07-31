from ROOT import TFile, TCanvas, TH1F
import numpy
import glob

file_list = glob.glob('../ntuple/*.root')

h_topmass= TH1F('TopMass','TopMass',200,160.,190.)
h_antitopmass= TH1F('AntiTopMass','AntiTopMass',200,160.,190.)

for filename in file_list:
	myfile = TFile(filename,"READ")
	tree = myfile.Get("MyLCTuple")
	print filename
	for event in tree:
		ip=0
		topfound=0
		antitopfound=0
		for pdgId in tree.mcpdg:
			if pdgId==6:
				h_topmass.Fill(tree.mcmas[ip])
			if pdgId==-6:
				h_antitopmass.Fill(tree.mcmas[ip])
			ip = ip+1
	iev=iev+1
	
c_topmass=TCanvas('TopMass','TopMass',800,800)
c_topmass.cd()
h_topmass.Draw()

c_antitopmass=TCanvas('AntiTopMass','AntiTopMass',800,800)
c_antitopmass.cd()
h_antitopmass.Draw()


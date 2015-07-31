from ROOT import TFile, TCanvas, TH1F
import glob

#this script loop on the ntuples and produces the histograms of the id of the montecarlo particle WITH STATUS 1, the energy of the electrons and of the muons WITH STATUS 1.
#In addition this produces the same plots for reconstructed particles.

#declaration of the histograms

#montecarlo with st1
h_part_ID_st1 = TH1F("h_part_ID_st1","Particles_ID_st1",50000,-2500,2500); # Particle ID Histogram Particle with status = 1

h_EN_el_st1 = TH1F("h_EN_el_st1", "Energy of the electrons_st1", 150,0,150);  # Energy of the electron with status = 1

h_EN_mu_st1 = TH1F("h_EN_mu_st1", "Energy of the muons_st1", 150,0,150); #energy of the mu with status = 1

#reconstructed
h_part_ID_rc = TH1F("h_part_ID_rc","Particles_ID_rc",50000,-2500,2500); # Particle ID Histogram of the reconstructed particles

h_EN_el_rc = TH1F("h_EN_el_rc", "Energy of the electrons reconstructed", 150,0,150);  # Energy of the electron of the reconstructed particles

h_EN_mu_rc = TH1F("h_EN_mu_rc", "Energy of the muons reconstructed", 150,0,150); #energy of the mu of the reconstructed particles

#loop on the ntuples

file_list = glob.glob('./../ntuple/*.root')

for filename in file_list:
	myfile = TFile(filename,"READ")
	tree = myfile.Get("MyLCTuple")
	iev = 0
	for event in tree:
		print 'Event ',iev
		iev = iev + 1
		
		#montecarlo with status 1
		ip = 0
		for pdgId in tree.mcpdg:
			if (pdgId>-2500 and pdgId<2500) and tree.mcgst[ip]==1:
				h_part_ID_st1.Fill(pdgId)
			if (pdgId==11 or pdgId==-11) and tree.mcgst[ip]==1:
				h_EN_el_st1.Fill(tree.mcene[ip])
			if (pdgId==13 or pdgId==-13) and tree.mcgst[ip]==1:
				h_EN_mu_st1.Fill(tree.mcene[ip])
			ip=ip+1
			
		#reconstructed
		ip = 0
		for pdgId in tree.rctyp:
			if pdgId>-2500 and pdgId<2500:
				h_part_ID_rc.Fill(pdgId)
			if pdgId==11 or pdgId==-11:
				h_EN_el_rc.Fill(tree.rcene[ip])
			if pdgId==13 or pdgId==-13:
				h_EN_mu_rc.Fill(tree.rcene[ip])
			ip = ip+1

#saving histograms
mcst1_rc_e_mu_EN_histo = TFile("./../plot/mcst1_rc_e_mu_EN_histo.root","CREATE")

h_part_ID_st1.Write()
h_EN_el_st1.Write()
h_EN_mu_st1.Write()

h_part_ID_rc.Write()
h_EN_el_rc.Write()
h_EN_mu_rc.Write()

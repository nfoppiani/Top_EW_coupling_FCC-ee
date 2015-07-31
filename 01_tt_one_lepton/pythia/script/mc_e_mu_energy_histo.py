from ROOT import TFile, TCanvas, TH1F
import glob

#this script loop on the ntuples and produces the histograms of the id of the montecarlo particles, the energy of the electrons and of the muons.

#declaration of the histograms 

h_part_ID = TH1F("h_part_ID","Particles_ID",50000,-2500,2500); # Particle ID Histogram

h_EN_el = TH1F("h_EN_el", "Energy of the electrons", 150,0,150);  # Energy of the electron

h_EN_mu = TH1F("h_EN_mu", "Energy of the muons", 150,0,150); #energy of the mu

#loop on the ntuples

file_list = glob.glob('./../ntuple/*.root')

for filename in file_list:
	myfile = TFile(filename,"READ")
	tree = myfile.Get("MyLCTuple")
	iev = 0
	for event in tree:
		print 'Event ',iev
		iev = iev + 1
		ip = 0
		for pdgId in tree.mcpdg:
			if pdgId>-2500 and pdgId<2500:
				h_part_ID.Fill(pdgId)
			if pdgId==11 or pdgId==-11:
				h_EN_el.Fill(tree.mcene[ip])
			if pdgId==13 or pdgId==-13:
				h_EN_mu.Fill(tree.mcene[ip])
			#if 	(pdgId==11 or pdgId==-11) and tree.mcene[ip]>13:
			#	good_leptons = good_leptons +1
			#if 	(pdgId==13 or pdgId==-13) and tree.mcene[ip]>13:
			#	good_leptons = good_leptons +1	
			ip = ip+1
	myfile.Close()
       # e = tree.mcene[ip]
       # px = tree.mcmox[ip]
       # py = tree.mcmoy[ip]
       # pz = tree.mcmoz[ip]
       # print ip,pdgId,px,py,pz,e

#print good_leptons

c_Part_ID = TCanvas("Part_ID","canvas1",800,800);  
c_EN_el = TCanvas("EN_el","canvas2",800,800);  
c_EN_mu = TCanvas("EN_mu","canvas3",800,800);   

c_Part_ID.cd();
h_part_ID.Draw();  

c_EN_el.cd();
h_EN_el.Draw();
 
c_EN_mu.cd();
h_EN_mu.Draw();


#saving histograms
mc_e_mu_energy_histo = TFile("./../plot/mc_e_mu_energy_histo.root","CREATE")
h_part_ID.Write()
h_EN_el.Write()
h_EN_mu.Write()

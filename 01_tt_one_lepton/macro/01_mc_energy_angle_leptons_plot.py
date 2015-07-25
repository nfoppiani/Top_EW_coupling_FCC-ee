from ROOT import TFile, TCanvas, TH1F

file = TFile("ntuple1.root","READ")
tree = file.Get("MyLCTuple")

h_part_ID = TH1F("h_part_ID","Particles_ID",50000,-25000,25000); # Particle ID Histogram

h_EN_el = TH1F("h_EN_el", "Energy of the electrons", 100,0,100);  # Energy of the electron
#h_ang_el = TH1F("h_ang_el", "angle of the electrons", ,0,100); # angle of the electron
h_EN_mu = TH1F("h_EN_mu", "Energy of the muons", 100,0,100); #energy of the mu
#TH1F *h_ang_mu; //angle of the mu

good_leptons = 0
iev = 0
for event in tree:
    print 'Event ',iev
    iev = iev + 1
    ip = 0
    for pdgId in tree.mcpdg:
		if pdgId>-25000 and pdgId<25000:
			h_part_ID.Fill(pdgId)
		if pdgId==11 or pdgId==-11:
			h_EN_el.Fill(tree.mcene[ip])
		if pdgId==13 or pdgId==-13:
			h_EN_mu.Fill(tree.mcene[ip])
		if 	(pdgId==11 or pdgId==-11) and tree.mcene[ip]>13:
			good_leptons = good_leptons +1
		if 	(pdgId==13 or pdgId==-13) and tree.mcene[ip]>13:
			good_leptons = good_leptons +1	
       # e = tree.mcene[ip]
       # px = tree.mcmox[ip]
       # py = tree.mcmoy[ip]
       # pz = tree.mcmoz[ip]
       # print ip,pdgId,px,py,pz,e
		ip = ip+1
#	print
#print

print good_leptons

Part_ID = TCanvas("Part_ID","canvas1",800,800);  
EN_el = TCanvas("EN_el","canvas2",800,800);  
EN_mu = TCanvas("EN_mu","canvas3",800,800);   

Part_ID.cd();
h_part_ID.Draw();  

EN_el.cd();
h_EN_el.Draw();
 
EN_mu.cd();
h_EN_mu.Draw();

file_to_save1 = TFile("./file_to_save1.root","CREATE")
Part_ID.Write()
EN_el.Write()
EN_mu.Write()

file.Close()

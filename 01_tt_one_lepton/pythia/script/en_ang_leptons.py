from ROOT import TFile, TCanvas, TH2F
import numpy
import glob

#definition of the histograms

h_EL = TH2F("Electrons","Electrons",16,0.,1.,16,-1.,1.)
h_MU = TH2F("Muons","Muons",16,0.,1.,16,-1.,1.)
h_ELplusMU = TH2F("Electrons+Muons","Electrons+Muons",16,0.,1.,16,-1.,1.)

#variables

m_t =173.1
s=365**2
beta_t=numpy.sqrt(1-4*(m_t)**2/s)
B=numpy.sqrt((1-beta_t)/(1+beta_t))
reducing_factor=(2/m_t)*B
print "beta_t =", beta_t

file_list = glob.glob('./../ntuple/*.root')

#filling the histograms

for filename in file_list:
	myfile = TFile(filename,"READ")
	tree = myfile.Get("MyLCTuple")
	print filename
	#iev = 0
	for event in tree:
	    #print 'Event ',iev
	    #iev = iev + 1
	    ip = 0
	    for pdgId in tree.mcpdg:
			#search for the electrons
			if pdgId==11 or pdgId==-11:
				#definition of parents
				pa0 = tree.mcpa0[ip]
				pa1 = tree.mcpa1[ip]
				if pa0 != -1:
					if tree.mcpdg[pa0]==24 or tree.mcpdg[pa0]==-24:
						energy=tree.mcene[ip]
						r_energy= energy*reducing_factor
						cosTheta=(tree.mcmoz[ip]/numpy.sqrt(tree.mcmox[ip]**2+tree.mcmoy[ip]**2+tree.mcmoz[ip]**2))
						h_EL.Fill(r_energy,cosTheta)
						h_ELplusMU.Fill(r_energy,cosTheta)
				if pa1 != -1:
					if tree.mcpdg[pa1]==24 or tree.mcpdg[pa1]==-24:
						energy=tree.mcene[ip]
						r_energy= energy*reducing_factor
						cosTheta=(tree.mcmoz[ip]/numpy.sqrt(tree.mcmox[ip]**2+tree.mcmoy[ip]**2+tree.mcmoz[ip]**2))
						h_EL.Fill(r_energy,cosTheta)	
						h_ELplusMU.Fill(r_energy,cosTheta)
						
			#search for the muons
			if pdgId==13 or pdgId==-13:
				#definition of parents
				pa0 = tree.mcpa0[ip]
				pa1 = tree.mcpa1[ip]
				if pa0 != -1:
					if tree.mcpdg[pa0]==24 or tree.mcpdg[pa0]==-24:
						energy=tree.mcene[ip]
						r_energy= energy*reducing_factor
						cosTheta=(tree.mcmoz[ip]/numpy.sqrt(tree.mcmox[ip]**2+tree.mcmoy[ip]**2+tree.mcmoz[ip]**2))
						h_MU.Fill(r_energy,cosTheta)
						h_ELplusMU.Fill(r_energy,cosTheta)
				if pa1 != -1:
					if tree.mcpdg[pa1]==24 or tree.mcpdg[pa1]==-24:
						energy=tree.mcene[ip]
						r_energy= energy*reducing_factor
						cosTheta=(tree.mcmoz[ip]/numpy.sqrt(tree.mcmox[ip]**2+tree.mcmoy[ip]**2+tree.mcmoz[ip]**2))
						h_MU.Fill(r_energy,cosTheta)	
						h_ELplusMU.Fill(r_energy,cosTheta)
			ip=ip+1


#plotting the histograms

c_EL = TCanvas("Electrons","Electrons",800,800)
c_EL.cd()
h_EL.Draw("surf")

c_MU = TCanvas("Muons","Muons",800,800)
c_MU.cd()
h_MU.Draw("surf")

c_ELplusMU = TCanvas("Electrons+muons","Electrons+muons",800,800)
c_ELplusMU.cd()
h_ELplusMU.Draw("surf")

#saving the histograms

print "I am saving the histos"

mc_e_mu_energy_histo = TFile("./../plot/lepton_distribution_histo.root","CREATE")
h_EL.Write()
h_MU.Write()
h_ELplusMU.Write()

#saving the canvas

mc_e_mu_energy_histo = TFile("./../plot/lepton_distribution_canvas.root","CREATE")
c_EL.Write()
c_MU.Write()
c_ELplusMU.Write()

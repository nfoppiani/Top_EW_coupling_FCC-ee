from ROOT import TFile, TCanvas, TH2F
import numpy
import glob

#definition of the histograms

h_EL = TH2F("Electrons","Electrons",16,0.,1.,16,-1.,1.)


#variables

m_t =173.1
s=365**2
beta_t=numpy.sqrt(1-4*(m_t)**2/s)
B=numpy.sqrt((1-beta_t)/(1+beta_t))
reducing_factor=(2/m_t)*B
print "beta_t =", beta_t

file_list = glob.glob('.root')

iev=0

for filename in file_list:
	myfile = TFile(filename,"READ")
	tree = myfile.Get("MyLCTuple")
	print filename
	for event in tree:
		if tree.mcpdg[10]!=11:
			print ERRRORE! la particella 10 non è un elettrone!!!
		if tree.mcpdg[10]==11:
			energy=tree.mcene[10]
			r_energy= energy*reducing_factor
			cosTheta=(tree.mcmoz[10]/numpy.sqrt(tree.mcmox[10]**2+tree.mcmoy[10]**2+tree.mcmoz[10]**2))
			h_EL.Fill(r_energy,cosTheta)
	iev=iev+1
	
c_EL = TCanvas("Electrons","Electrons",800,800)
c_EL.cd()
h_EL.Draw("surf")

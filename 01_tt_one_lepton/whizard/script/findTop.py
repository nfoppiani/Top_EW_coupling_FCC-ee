from ROOT import TFile, TCanvas, TH1F
import numpy
import glob

file_list = glob.glob('../ntuple/*.root')

h_topmass= TH1F('TopMass','TopMass',150,164.,183.)
h_antitopmass= TH1F('AntiTopMass','AntiTopMass',150,164.,183.)


iev=0
numeroWmeno =0
numero_ele=0
numero_t=0
numero_at=0

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
				numero_t=numero_t+1
				h_topmass.Fill(tree.mcmas[ip])
				topfound=topfound+1
			if pdgId==-6:
				numero_at=numero_at+1
				h_antitopmass.Fill(tree.mcmas[ip])
				antitopfound=antitopfound+1
			if pdgId==-24:
				numeroWmeno=numeroWmeno +1
			if pdgId==11:
				#definition of parents
				pa0 = tree.mcpa0[ip]
				pa1 = tree.mcpa1[ip]
				if pa0 != -1:
					if tree.mcpdg[pa0]==-24:
						numero_ele=numero_ele+1
					#if tree.mcpdg[pa0]!=-24:
						#print "The parent isn't a W but a ", tree.mcpdg[pa0]
				if pa1 != -1:
					if tree.mcpdg[pa1]==-24:
						numero_ele=numero_ele+1
					#if tree.mcpdg[pa1]!=-24:
						#print "The parent isn't a W but a ", tree.mcpdg[pa1]
			ip = ip+1
		if antitopfound ==2:
				print "strange event", filename, iev
	iev=iev+1

print "numero_ele =", numero_ele
print "numeroWmeno =", numeroWmeno

print "numero top =", numero_t
print "numero antitop =", numero_at


c_topmass=TCanvas('TopMass','TopMass',800,800)
c_topmass.cd()
h_topmass.Draw()

c_antitopmass=TCanvas('AntiTopMass','AntiTopMass',800,800)
c_antitopmass.cd()
h_antitopmass.Draw()

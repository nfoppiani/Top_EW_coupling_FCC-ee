from ROOT import TFile, TCanvas, TH2F
import numpy
import glob

file_list = glob.glob('../ntuple/*.root')

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
		for pdgId in tree.mcpdg:
			if pdgId==6:
				numero_t=numero_t+1
			if pdgId==-6:
				numero_at=numero_at+1
			if pdgId==-24:
				numeroWmeno=numeroWmeno +1
			if pdgId==11:
				#definition of parents
				pa0 = tree.mcpa0[ip]
				pa1 = tree.mcpa1[ip]
				if pa0 != -1:
					if tree.mcpdg[pa0]==-24:
						numero_ele=numero_ele+1
					if tree.mcpdg[pa0]!=-24:
						print "The parent isn't a W but a ", tree.mcpdg[pa0]
				if pa1 != -1:
					if tree.mcpdg[pa1]==-24:
						numero_ele=numero_ele+1
					if tree.mcpdg[pa1]!=-24:
						print "The parent isn't a W but a ", tree.mcpdg[pa1]
			ip = ip+1
	iev=iev+1

print "numero_ele =", numero_ele
print "numeroWmeno =", numeroWmeno

print "numero top =", numero_t
print "numero antitop =", numero_at

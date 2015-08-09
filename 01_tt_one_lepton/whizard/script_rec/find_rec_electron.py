from ROOT import TFile, TCanvas, TH1F, TTree
import numpy

myfile = TFile.Open("../ntuple/prova/yyxyev_o_1.root")
tree = myfile.Get("MyLCTuple")

h_distance=TH1F("distance from mc_electrons","distance from mc_electrons",100,0.,100.)
h_type=TH1F("type of the minimum distance particle","type of the minimum distance particle",50000,-2500.,2500.)
h_deltaE=TH1F("delta energy of the minimum distance particle","delta energy of the minimum distance particle",150,-100.,100.)

ene_mc=0.
px_mc=0.
py_mc=0.
pz_mc=0.

distance=0.
distance_aux=0.

ene=0.
px=0.
py=0.
pz=0.

rc_type=0.

deltaE=0.

for event in tree:
	ene_mc=tree.mcene[10]
	px_mc=tree.mcmox[10]
	py_mc=tree.mcmoy[10]
	pz_mc=tree.mcmoz[10]
	distance=0.
	distance_aux=0.
	rc_type=0
	for ind in range(len(tree.rctyp)):
		#if tree.rctyp[ind]!=22:			
		ene=tree.rcene[ind]
		px=tree.rcmox[ind]
		py=tree.rcmoy[ind]
		pz=tree.rcmoz[ind]
		distance_aux=(ene-ene_mc)**2+(px-px_mc)**2+(py-py_mc)**2+(pz-pz_mc)**2
		if distance==0. or distance_aux<distance:
			distance=distance_aux
			rc_type=tree.rctyp[ind]	
			deltaE=ene_mc-ene
	h_distance.Fill(numpy.sqrt(distance))
	h_type.Fill(rc_type)
	h_deltaE.Fill(deltaE)


a=TCanvas("ciao","ciao",800,800)
a.cd()
h_distance.Draw()

b=TCanvas("ciao2","ciao2",800,800)
b.cd()
h_type.Draw()
	
c=TCanvas("ciao3","ciao3",800,800)
c.cd()
h_deltaE.Draw()

#savingFile = TFile("../plot/electrons_histo.root", "CREATE")

#savingFile.cd()
#h_mc.Write()      
#savingFile.Close()


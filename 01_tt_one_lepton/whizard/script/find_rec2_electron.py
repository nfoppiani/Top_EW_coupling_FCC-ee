from ROOT import TFile, TCanvas, TH1F, TH2F, TTree, TChain
import numpy

tree = TChain("MyLCTuple")
tree.Add("../ntuple/prova/yyxyev_o_*.root")


h_distance=TH1F("distance from mc_electrons","distance from mc_electrons",100,0.,100.)
h_type=TH1F("type of the minimum distance particle","type of the minimum distance particle",50000,-2500.,2500.)
h_deltaE=TH1F("delta energy of the minimum distance particle","delta energy of the minimum distance particle",150,-100.,100.)

h_deltaE_jet=TH1F("delta energy of the minimum distance jet","delta energy of the minimum distance jet",150,-100.,100.)
h_cosfi=TH1F("cosfi of the minimum distance jet","cosfi of the minimum distance jet",20,-1.,1.)

h_photons=TH2F("energy-angle-photons","energy-angle-photons",100,0.,100.,20,-1.,1.)

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
deltaE_jet=0.
cosfi=0.

jene=0.
jpx=0.
jpy=0.
jpz=0.

for event in tree:
	ene_mc=tree.mcene[10]
	px_mc=tree.mcmox[10]
	py_mc=tree.mcmoy[10]
	pz_mc=tree.mcmoz[10]
	distance=0.
	distance_aux=0.
	rc_type=0
	cosfi=0.
	#loop above particles
	for ind in range(len(tree.rctyp)):
		good_index=0
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
			good_index=ind
	h_distance.Fill(numpy.sqrt(distance))
	h_type.Fill(rc_type)
	h_deltaE.Fill(deltaE)
	if rc_type==22:
		h_photons.Fill(tree.rcene[good_index],(px_mc*tree.rcmox[good_index]+py_mc*tree.rcmoy[good_index]+pz_mc*tree.rcmoz[good_index])/(numpy.sqrt(px_mc**2+py_mc**2+pz_mc**2)*tree.rcene[good_index]))
	#loop above jets
	cosfi=0.
	deltaE_jet=0.
	for ind in range(len(tree.jene)):
		jene=tree.jene[ind]
		jpx=tree.jmox[ind]
		jpy=tree.jmoy[ind]
		jpz=tree.jmoz[ind]
		cosfi_aux=(px_mc*jpx+py_mc*jpy+pz_mc*jpz)/(numpy.sqrt(px_mc**2+py_mc**2+pz_mc**2)*numpy.sqrt(jpx**2+jpy**2+jpz**2))
		if cosfi_aux>1:
			print "ERROR, cosfi>1",cosfi_aux
		if cosfi_aux>cosfi:
			cosfi=cosfi_aux
			deltaE_jet=ene_mc-jene
	h_deltaE_jet.Fill(deltaE_jet)
	h_cosfi.Fill(cosfi)
	
c_distance=TCanvas("Distance in phase space from montecarlo electron","Distance in phase space from montecarlo electron",800,800)
c_distance.cd()
h_distance.Draw()

c_type=TCanvas("type of the minimum distance particle","type of the minimum distance particle",800,800)
c_type.cd()
h_type.Draw()
	
c_deltaE=TCanvas("delta energy of the minimum distance particle","delta energy of the minimum distance particle",800,800)
c_deltaE.cd()
h_deltaE.Draw()

c_deltaE_jet=TCanvas("delta energy of the minimum distance jet","delta energy of the minimum distance jet",800,800)
c_deltaE_jet.cd()
h_deltaE_jet.Draw()

c_cosfi=TCanvas("cosfi of the minimum distance jet","cosfi of the minimum distance jet",800,800)
c_cosfi.cd()
h_cosfi.Draw()

c_photons=TCanvas("photons","photons",800,800)
c_photons.cd()
h_photons.Draw()
#savingFile = TFile("../plot/electrons_histo.root", "CREATE")

#savingFile.cd()
#h_mc.Write()      
#savingFile.Close()

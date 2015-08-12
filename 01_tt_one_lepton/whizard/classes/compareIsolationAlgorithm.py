from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *
from findElectrons import *

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/electrons_ntuple/yyxyev_o_*.root')

errPt=0
errCha=0

for event in tree:
        
	rcParticles = []
	for i in range(len(tree.rctyp)):
		p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
		rcParticles.append(p)
	

	rcJets = []
	for i in range(len(tree.jene)):
		p = Jet(i,tree.jmas[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
		rcJets.append(p)
	
	mcElectron = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])
	Match=[]
	Match=mcElectron.matchElectron(rcParticles)
	numPt=findElectronPtMaxClosestJet(rcParticles,rcJets)
	numCha=findElectronConeChargedNotElectronParticle(rcParticles)
	
	if Match[0] != numPt:
		errPt = errPt + 1
	if Match[1] != numCha:
		errCha=errCha+1

print "errPt", errPt
print "errCha", errCha
	

from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *
from findElectrons import *

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/electrons_ntuple/yyxyev_o_*.root')

errPt=0
errCha=0

hEnergyDifference=TH1F("Energy matched - energy montecarlo","Energy matched - energy montecarlo",100,-50.,50.)
hcosTheta=TH1F("CosTheta matched,montecarlo","CosTheta matched,montecarlo",20,-1.,1.)
hDistance=TH1F("Distance between matched and montecarlo particle","Distance between matched and montecarlo particle",100,0.,100.)

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

	hEnergyDifference.Fill(rcParticles[Match[0]].p.E()-mcElectron.p.E())
	hcosTheta.Fill(mcElectron.cos(rcParticles[Match[0]]))
	hDistance.Fill(Match[1])
	
savingFile=TFile('./../plot/matchingTest.root',"RECREATE")
savingFile.cd()
hEnergyDifference.Write()
hcosTheta.Write()
hDistance.Write()

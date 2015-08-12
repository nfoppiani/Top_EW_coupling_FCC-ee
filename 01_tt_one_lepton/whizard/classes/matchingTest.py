from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *
from findElectrons import *

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')

errPt=0
errCha=0

hEnergyDifference=TH1F("Energy matched - energy montecarlo","Energy matched - energy montecarlo",100,-50.,50.)
hTheta=TH1F("Theta matched,montecarlo","Theta matched,montecarlo",200,-0.2,0.2)
hDistance=TH1F("Distance between matched and montecarlo muon","Distance between matched and montecarlo muon",100,0.,100.)

#hType=TH1F("type of closest particle","type of closest particle",50000,-250,3000)

for event in tree:
	if tree.mcpdg[10]==13:
		mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])
	
		rcParticles = []
		for i in range(len(tree.rctyp)):
			p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
			rcParticles.append(p)

                rcJets = []
		for i in range(len(tree.jene)):
			p = Jet(i,tree.jmas[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
			rcJets.append(p)

		#rcJets = []
		#for i in range(len(tree.jene)):
			#p = Jet(i,tree.jmas[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
			#rcJets.append(p)
	
	
		MatchNum=mcMuon.matchMuon(rcParticles)

                print mcMuon.ptToClosestJet(rcJets)
		hEnergyDifference.Fill(rcParticles[MatchNum].p.E()-mcMuon.p.E())
		hTheta.Fill(mcMuon.angle(rcParticles[MatchNum]))
		hDistance.Fill(Distance(mcMuon,rcParticles[MatchNum]))
		
		#hType.Fill(rcParticles[MatchNum].type)

savingFile=TFile('./../plot/matchingTestMuons.root',"RECREATE")
savingFile.cd()
hEnergyDifference.Write()
hTheta.Write()
hDistance.Write()
#hType.Write()

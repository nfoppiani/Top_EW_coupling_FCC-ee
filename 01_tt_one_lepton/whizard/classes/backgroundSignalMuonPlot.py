from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *
from findElectrons import *

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')

#declaration of histograms

hPtClosestJet=TH1F("Pt to the closest Jet","Pt to the closest Jet",100,0.,100.)

hPtPartial1=TH1F("Pt to the closest Jet signal","Pt to the closest Jet signal",100,0.,100.)

hPtPartial2=TH1F("Pt to the closest Jet bg","Pt to the closest Jet bg",100,0.,100.)


hAngleClosestCharge=TH1F("Angle to the closest charged particle","Angle to the closest charged particle",100,0.,1.)

hAnglePartial1=TH1F("Angle to the closest charged particle signal","Angle to the closest charged particle signal",100,0.,1.)

hAnglePartial2=TH1F("Angle to the closest charged particle bg","Angle to the closest charged particle bg",100,0.,1.)


hPtJetAngleChar=TH2F("Pt to the closest Jet, Angle to the closest charged particle","Pt to the closest Jet, Angle to the closest charged particle",100,0.,100.,100,0.,1.)

hPtJetAngleCharPartial1=TH2F("Pt to the closest Jet, Angle to the closest charged particle SIGNAL","Pt to the closest Jet, Angle to the closest charged particle SIGNAL",100,0.,100.,100,0.,1.)

hPtJetAngleCharPartial2=TH2F("Pt to the closest Jet, Angle to the closest charged particle BG","Pt to the closest Jet, Angle to the closest charged particle BG",100,0.,100.,100,0.,1.)

Pt=0.
Angle=0.

#loop on the events
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
	
		MatchNum=mcMuon.matchMuon(rcParticles)
		
		Pt=rcParticles[MatchNum].ptToClosestJet(rcJets)
		hPtPartial1.Fill(Pt)
		
		Angle=rcParticles[MatchNum].angleToClosestCharge(rcParticles)
		hAnglePartial1.Fill(Angle)
		
		hPtJetAngleCharPartial1.Fill(Pt,Angle)
		
		for part in rcParticles:
			if part.type ==13 and part.num!=MatchNum:
				Pt=part.ptToClosestJet(rcJets)
				hPtPartial2.Fill(Pt)
				
				Angle=part.angleToClosestCharge(rcParticles)
				hAnglePartial2.Fill(Angle)
				
				hPtJetAngleCharPartial2.Fill(Pt,Angle)

hPtPartial1.SetLineColor(2) #set the red fill color				
#hPtClosestJet.Add(hPtPartial1)

hPtPartial2.SetLineColor(3) #set the green fill color
#hPtClosestJet.Add(hPtPartial2)



hAnglePartial1.SetLineColor(2) #set the red fill color				
#hAngleClosestCharge.Add(hPtPartial1)

hAnglePartial2.SetLineColor(3) #set the green fill color
#hAngleClosestCharge.Add(hPtPartial2)



hPtJetAngleCharPartial1.SetLineColor(2) #set the red fill color				
#hPtJetAngleChar.Add(hPtJetAngleCharPartial1)

hPtJetAngleCharPartial2.SetLineColor(3) #set the green fill color
#hPtJetAngleChar.Add(hPtJetAngleCharPartial2)


hPtJetAngleCharPartial1.Draw("Lego")
hPtJetAngleCharPartial2.Draw("Lego","same")

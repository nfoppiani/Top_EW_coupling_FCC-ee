from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain, THStack
import numpy
from particleClass import *
from findElectrons import *

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')


PtMax=2.

coneCutAngle=numpy.deg2rad(5)

#declaration of histograms

hAngleEnergyJet=TH1F("Angle to the Jet weight with energy","Angle to the Jet weight with energy",100,0.,1.)

hEnergy=TH1F("Energy to the closest Jet signal","Energy the closest Jet signal",100,0.,100.)

hType=TH1F("Type of the closest Jet components","Type of the closest Jet components",10000,-2000,2500)

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
	
		matchNum=mcMuon.matchMuon(rcParticles)
                
                for jet in rcJets:
                        if mcMuon.p.Pt(jet.p.Vect())<PtMax:
                                for part in rcParticles:
                                        if part.angle(mcMuon)<coneCutAngle and part.num!=matchNum:
                                                hType.Fill(part.type)


hType.Draw()


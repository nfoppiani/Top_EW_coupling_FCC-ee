from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain, THStack
import numpy
from particleClass import *
from findElectrons import *

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')

#declaration of histograms

hAngleEnergyJet=TH1F("Angle to the Jet weight with energy","Angle to the Jet weight with energy",100,0.,1.)

hEnergy=TH1F("Energy to the closest Jet signal","Energy the closest Jet signal",100,0.,100.)

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
	
		EneJet=0.
                for jet in rcJets:
                        minJet=0.
                        EneJet=0.
                        if mcMuon.p.Pt(jet.p.Vect())<minJet or minJet==0.:
                                minJet=mcMuon.p.Pt(jet.p.Vect())
                                EneJet=jet.p.E()
                        hAngleEnergyJet.Fill(jet.angle(mcMuon),jet.p.E())


hEnergy.Draw()


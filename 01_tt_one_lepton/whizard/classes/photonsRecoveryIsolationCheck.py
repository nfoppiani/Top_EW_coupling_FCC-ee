from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

tree = TChain("MyLCTuple")

#tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')
tree.Add('./../whizard_negMuTau_yyxylv/000/yyxylv_o_*.root')
tree.Add('./../whizard_negMuTau_yyxylv/001/yyxylv_o_*.root')

def energyInAngleWithoutPhotons(mu,ang,rcList):
    energy = 0
    for part in rcList:
        if part.typ != 22 and mu.angle(part) < numpy.radians(ang) and part.num != mu.num and part.status:
            energy += part.p.E()
    return energy

hConeEnergyW10 = TH1F("coneEnergyW10", "Energy in a 10 degrees cone", 300, 0., 150.)
hConeEnergyNotW10 = TH1F("coneEnergyNotW10", "Energy in a 10 degrees cone", 300, 0., 150.)
hConeEnergyW15 = TH1F("coneEnergyW15", "Energy in a 15 degrees cone", 300, 0., 150.)
hConeEnergyNotW15 = TH1F("coneEnergyNotW15", "Energy in a 15 degrees cone", 300, 0., 150.)
hConeEnergyW20 = TH1F("coneEnergyW20", "Energy in a 20 degrees cone", 300, 0., 150.)
hConeEnergyNotW20 = TH1F("coneEnergyNotW20", "Energy in a 20 degrees cone", 300, 0., 150.)

k = 0

for event in tree:
    if k % 990 == 0:
        print 'file ', k/99
    k += 1
    
    if tree.mcpdg[10]==13:
        mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10],1)
        
        rcParticles = []
        rcMuons = []
        for i in range(len(tree.rctyp)):
            p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i],1)
            rcParticles.append(p)
            if p.typ == 13:
                rcMuons.append(p)

        matchNum = mcMuon.matchMuon(rcParticles)
        
        for muon in rcMuons:
            energy10 = energyInAngleWithoutPhotons(muon,10,rcParticles)
            energy15 = energyInAngleWithoutPhotons(muon,15,rcParticles)
            energy20 = energyInAngleWithoutPhotons(muon,20,rcParticles)
            if muon.num == matchNum:
                hConeEnergyW10.Fill(energy10)
                hConeEnergyW15.Fill(energy15)
                hConeEnergyW20.Fill(energy20)
            else:
                hConeEnergyNotW10.Fill(energy10)
                hConeEnergyNotW15.Fill(energy15)
                hConeEnergyNotW20.Fill(energy20)

savingFile=TFile('./photonsRecoveryIsolationCheck.root',"RECREATE")
savingFile.cd()
hConeEnergyW10.Write()
hConeEnergyNotW10.Write()
hConeEnergyW15.Write()
hConeEnergyNotW15.Write()
hConeEnergyW20.Write()
hConeEnergyNotW20.Write()
savingFile.Close()
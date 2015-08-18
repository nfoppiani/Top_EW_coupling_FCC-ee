from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

tree = TChain("MyLCTuple")

#tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')
tree.Add('./../whizard_negMuTau_yyxylv/000/yyxylv_o_*.root')
tree.Add('./../whizard_negMuTau_yyxylv/001/yyxylv_o_*.root')

hPhotonDistributionW = TH2F("photonDistributionW", "Emitted photons distribution", 140, 0., 70., 40, 0., 20.)
hPhotonDistributionNotW = TH2F("photonDistributionNotW", "Emitted photons distribution", 140, 0., 70., 40, 0., 20.)

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
        
        if matchNum != -1 and rcParticles[matchNum].typ == 13:
            matchedMuon = rcParticles[matchNum]

            for photon in rcParticles:
                if photon.typ == 22 and photon.status:
                    angle = photon.angle(matchedMuon)
                    if angle < numpy.radians(20):
                        hPhotonDistributionW.Fill(photon.energy(), numpy.degrees(angle))
        
        for muon in rcMuons:
            if muon.num != matchNum:
                for photon in rcParticles:
                    if photon.typ == 22 and photon.status:
                        angle = photon.angle(muon)
                        if angle < numpy.radians(20):
                            hPhotonDistributionNotW.Fill(photon.energy(), numpy.degrees(angle))

savingFile=TFile('./photonsAngleEnergyDistribution.root',"RECREATE")
savingFile.cd()
hPhotonDistributionW.Write()
hPhotonDistributionNotW.Write()
savingFile.Close()
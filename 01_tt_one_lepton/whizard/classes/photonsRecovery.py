from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

tree = TChain("MyLCTuple")

tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_798.root')
#tree.Add('./../whizard_negMuTau_yyxylv/000/yyxylv_o_*.root')
#tree.Add('./../whizard_negMuTau_yyxylv/001/yyxylv_o_*.root')

hBefore = TH1F("energyDifferenceBefore","Energy matched - energy montecarlo before recovery",500,-100.,100.)
hAfter = TH1F("energyDifferenceAfter","Energy matched - energy montecarlo after recovery",500,-100.,100.)

k = 0

for event in tree:
    #print 'EVENT ', k
    if k % 990 == 0:
        print 'file ', k/99
    if tree.mcpdg[10]==13:
        mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10],1)
        
        rcMuons = []
        rcParticles = []
        for i in range(len(tree.rctyp)):
            p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i],1)
            rcParticles.append(p)
            if p.typ == 13:
                rcMuons.append(p)
    
        matchNum = mcMuon.matchMuon(rcParticles)
        
        for muon in rcMuons:
            muon.photonsRecovery(rcParticles)
            rcParticles[muon.num] = muon
            if muon.num == matchNum:
                print 'EVENT ', k, muon.energy()-mcMuon.energy()
                print muon.energy(), mcMuon.energy()
                hAfter.Fill(muon.energy() - mcMuon.energy())
                if abs(muon.energy()-mcMuon.energy())>40:
                    print 'FILE ', k/99 +1
                    print 'EVENT ', k%99, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                            
    k += 1

savingFile=TFile('./photonsRecovery.root',"RECREATE")
hBefore.Write()
hAfter.Write()
savingFile.Close()
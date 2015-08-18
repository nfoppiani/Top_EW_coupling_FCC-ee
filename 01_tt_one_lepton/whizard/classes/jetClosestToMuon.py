from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

maxInvMass = 11.

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')
#tree.Add('./../whizard_negMuTau_yyxylv/000/yyxylv_o_*.root')
#tree.Add('./../whizard_negMuTau_yyxylv/001/yyxylv_o_*.root')

hClosestJetAngleW = TH1F("closestJetAngleW", "Angle to the closest jet", 240 ,0.,120.)
hClosestJetAngleNotW = TH1F("closestJetAngleNotW", "Angle to the closest jet", 240 ,0.,120.)
hMassWithClosestJetW = TH1F("invariantMassWithClosestJetW","Invariant mass with muon closest jet",300,-100.,100.)
hMassWithClosestJetNotW = TH1F("invariantMassWithClosestJetNotW","Invariant mass with muon closest jet",300,-100.,100.)
hSelectedJetEnergyWithoutMuonW = TH1F("selectedJetEnergyWithoutMuonW","Energy of muon-jets without the muons",400,-100.,100.)
hSelectedJetEnergyWithoutMuonNotW = TH1F("selectedJetEnergyWithoutMuonNotW","Energy of muon-jets without the muons",400,-100.,100.)
hSelectedJetBTagW = TH1F("muonJetBTagW", "B-tagging", 200, 0., 1.)
hSelectedJetBTagNotW = TH1F("muonJetBTagNotW", "B-tagging", 200, 0., 1.)

k = 0

for event in tree:
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
    
        rcJets = []
        for i in range(len(tree.jene)):
            p = TaggedJet(i,tree.jmas[i],tree.jcha[i],tree.jmox[i],tree.jmoy[i],tree.jmoz[i],tree.jene[i], tree.btag[i], tree.ctag[i],1)
            rcJets.append(p)

        matchNum = mcMuon.matchMuon(rcParticles)

        for muon in rcMuons:
            #muon.photonsRecovery(rcParticles)
            #rcParticles[muon.num] = muon

            invMass = -99
            realEnergy = -99
            btag = -1
            minAngle = numpy.pi
            for i in range(len(rcJets)):
                ang = rcJets[i].angle(muon)
                if ang < minAngle:
                    minAngle = ang
                    invMass = InvariantMass(muon, rcJets[i])
                    realEnergy = rcJets[i].energy()-muon.energy()
                    btag = rcJets[i].btag

            if muon.num == matchNum:
                hClosestJetAngleW.Fill(numpy.degrees(minAngle))
                hMassWithClosestJetW.Fill(invMass)
            else:
                hClosestJetAngleNotW.Fill(numpy.degrees(minAngle))
                hMassWithClosestJetNotW.Fill(invMass)
            
            if invMass < maxInvMass:
                if muon.num == matchNum:
                    hSelectedJetEnergyWithoutMuonW.Fill(realEnergy)
                    hSelectedJetBTagW.Fill(btag)
                else:
                    hSelectedJetEnergyWithoutMuonNotW.Fill(realEnergy)
                    hSelectedJetBTagNotW.Fill(btag)
    k = k+1

savingFile=TFile('./jetClosestToMuon.root',"RECREATE")
hClosestJetAngleW.Write()
hClosestJetAngleNotW.Write()
hMassWithClosestJetW.Write()
hMassWithClosestJetNotW.Write()
hSelectedJetEnergyWithoutMuonW.Write()
hSelectedJetEnergyWithoutMuonNotW.Write()
hSelectedJetBTagW.Write()
hSelectedJetBTagNotW.Write()
savingFile.Close()
from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

maxInvMass = 11.

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')
#tree.Add('./../whizard_negMuTau_yyxylv/000/yyxylv_o_*.root')
#tree.Add('./../whizard_negMuTau_yyxylv/001/yyxylv_o_*.root')

hMassWithClosestJet = TH1F("invariantMassWithClosestJet","Distance to muon closest jet",300,-30.,300.)
hMuonJetEnergyWithoutMuon = TH1F("muonJetEnergyWithoutMuon","Energy of muon-jets without the muons",800,-10.,30.)
hMuonJetBTag = TH1F("muonJetBTag", "B-tagging", 200, 0., 1.)

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

        for muon in rcMuons:
            muon.photonsRecovery(rcParticles)
            rcParticles[muon.num] = muon

            invMass = -20
            realEnergy = -20
            btag = -1
            minAngle = numpy.pi
            for i in range(len(rcJets)):
                ang = rcJets[i].angle(muon)
                if ang < minAngle:
                    minAngle = ang
                    invMass = InvariantMass(muon, rcJets[i])
                    realEnergy = rcJets[i].energy()-muon.energy()
                    btag = rcJets[i].btag

            hMassWithClosestJet.Fill(invMass)
            if invMass < maxInvMass:
                hMuonJetEnergyWithoutMuon.Fill(realEnergy)
                hMuonJetBTag.Fill(btag)
    k = k+1

savingFile=TFile('./jetMuonEnergy.root',"RECREATE")
hMassWithClosestJet.Write()
hMuonJetEnergyWithoutMuon.Write()
hMuonJetBTag.Write()
savingFile.Close()
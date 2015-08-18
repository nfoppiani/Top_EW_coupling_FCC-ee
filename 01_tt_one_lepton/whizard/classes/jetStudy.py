from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')
#tree.Add('./../whizard_negMuTau_yyxylv/000/yyxylv_o_*.root')
#tree.Add('./../whizard_negMuTau_yyxylv/001/yyxylv_o_*.root')

j = 0

for event in tree:
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
        if matchNum != -1:
            matchedMuon = rcParticles[matchNum]

        for muon in rcMuons:
            muon.photonsRecovery(rcParticles)
            rcParticles[muon.num] = muon

        for i in range(len(rcJets)):
            angle = rcJets[i].angle(mcMuon)
            if numpy.degrees(angle)<7 and numpy.degrees(angle)>4 and rcJets[i].cha == -1:
                print 'EVENT ', j
                print 'number\tcha\tene\t\tmox\t\tmoy\t\tmoz\t\tbtag\t\tctag\t\tangle'
                print 'muon', '\t', mcMuon.cha, '\t', mcMuon.p.E(),'\t', mcMuon.p.Px(),'\t', mcMuon.p.Py(),'\t', mcMuon.p.Pz()
                print 'RCmuon', '\t', matchedMuon.cha, '\t', matchedMuon.energy(),'\t', matchedMuon.p.Px(),'\t', matchedMuon.p.Py(),'\t', matchedMuon.p.Pz()
                print i, '\t', rcJets[i].cha, '\t', rcJets[i].p.E(),'\t', rcJets[i].p.Px(),'\t', rcJets[i].p.Py(),'\t', rcJets[i].p.Pz(), '\t', rcJets[i].btag, '\t', rcJets[i].ctag, '\t', numpy.degrees(angle)
                print
    j = j+1
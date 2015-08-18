# lists the W-decay mc muon, followed by the jets (and their angle with MC muon), for each event


from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_9*.root')

j = 0

for event in tree:
    if tree.mcpdg[10]==13:
        print 'EVENT ', j
        mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10],1)
        
#        rcMuons = []
#        k = 0
#        for i in range(len(tree.rctyp)):
#            if tree.rctyp[i] == 13:
#                p = Particle(k, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
#                rcMuons.append(p)
#                k = k+1

        rcJets = []
        for i in range(len(tree.jene)):
            p = TaggedJet(i,tree.jmas[i],tree.jcha[i],tree.jmox[i],tree.jmoy[i],tree.jmoz[i],tree.jene[i], tree.btag[i], tree.ctag[i],1)
            rcJets.append(p)

        print 'number\tcha\tene\t\tmox\t\tmoy\t\tmoz\t\tbtag\t\tctag\t\tangle'
        print 'muon', '\t', mcMuon.cha, '\t', mcMuon.p.E(),'\t', mcMuon.p.Px(),'\t', mcMuon.p.Py(),'\t', mcMuon.p.Pz()
        for i in range(len(rcJets)):
            angle = rcJets[i].angle(mcMuon)
            print i, '\t', rcJets[i].cha, '\t', rcJets[i].p.E(),'\t', rcJets[i].p.Px(),'\t', rcJets[i].p.Py(),'\t', rcJets[i].p.Pz(), '\t', rcJets[i].btag, '\t', rcJets[i].ctag, '\t', numpy.degrees(angle)
        print
    j = j+1
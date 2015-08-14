from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

file = TFile('./yyxylv_o_10.root',"READ")
tree = file.Get("MyLCTuple")

j = 0

for event in tree:
    if tree.mcpdg[10]==13:
        print 'EVENT ', j
        mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])
#        rcParticles = []
#        for i in range(len(tree.rctyp)):
#            p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
#            rcParticles.append(p)
        rcJets = []
        for i in range(len(tree.jene)):
            p = Jet(i,tree.jmas[i],tree.jcha[i],tree.jmox[i],tree.jmoy[i],tree.jmoz[i],tree.jene[i])
            rcJets.append(p)
    
        print 'number\tcha\tene\t\tmox\t\tmoy\t\tmoz\tangle'
        print 'muon', '\t', mcMuon.cha, '\t', mcMuon.p.E(),'\t', mcMuon.p.Px(),'\t', mcMuon.p.Py(),'\t', mcMuon.p.Pz()
        for i in range(len(rcJets)):
            angle = rcJets[i].angle(mcMuon)
            print i, '\t', rcJets[i].cha, '\t', rcJets[i].p.E(),'\t', rcJets[i].p.Px(),'\t', rcJets[i].p.Py(),'\t', rcJets[i].p.Pz(), '\t', angle
        print
    j = j+1
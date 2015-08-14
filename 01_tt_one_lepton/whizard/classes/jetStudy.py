from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

dtheta1Degrees = 0.8
dphi1Degrees = 0.8
dtheta2Degrees = 0.4
dphi2DegreesMax = 4.0
dphi2DegreesMin = -0.4

dtheta1 = numpy.radians(dtheta1Degrees)
dphi1 = numpy.radians(dphi1Degrees)
dtheta2 = numpy.radians(dtheta2Degrees)
dphi2Max = numpy.radians(dphi2DegreesMax)
dphi2Min = numpy.radians(dphi2DegreesMin)

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')
#tree.Add('./../whizard_negMuTau_yyxylv/000/yyxylv_o_*.root')
#tree.Add('./../whizard_negMuTau_yyxylv/001/yyxylv_o_*.root')

j = 0

for event in tree:
    if tree.mcpdg[10]==13:
        
        mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])
    
        rcParticles = []
        for i in range(len(tree.rctyp)):
            p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
            rcParticles.append(p)
    
        rcJets = []
        for i in range(len(tree.jene)):
            p = TaggedJet(i,tree.jmas[i],tree.jcha[i],tree.jmox[i],tree.jmoy[i],tree.jmoz[i],tree.jene[i], tree.btag[i], tree.ctag[i])
            rcJets.append(p)

        matchNum = mcMuon.matchMuon(rcParticles)
        if matchNum != -1:
            matchedMuon = rcParticles[matchNum]

        for photon in rcParticles:
            if photon.typ == 22:
                thetaDifference = photon.dtheta(matchedMuon)
                phiDifference = photon.dphi(matchedMuon)
                if abs(thetaDifference) < dtheta1:
                    if abs(phiDifference) < dphi1:
                        matchedMuon.p += photon.p
#                        print
#                        print 'recovered! ', matchedMuon.energy()-photon.energy(), ' to ', matchedMuon.energy()
                    else:
                        if abs(thetaDifference) < dtheta2:
                            if phiDifference > dphi2Min and phiDifference < dphi2Max:
                                matchedMuon.p += photon.p
#                                print
#                                print 'recovered!', matchedMuon.energy()-photon.energy(), ' to ', matchedMuon.energy()

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
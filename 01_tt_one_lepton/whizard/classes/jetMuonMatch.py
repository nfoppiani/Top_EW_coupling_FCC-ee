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

def invariantMass(a,b):
    return numpy.sqrt((a.energy()-b.energy())**2+(a.px()-b.px())**2+(a.py()-b.py())**2+(a.pz()-b.pz())**2)

hDistanceToClosestJet = TH1F("distanceClosestJet","Distance to muon closest jet",300,0.,300.)
hMassWithClosestJet = TH1F("invariantMassWithClosestJet","Distance to muon closest jet",300,-10.,300.)

j = 0

for event in tree:
    if tree.mcpdg[10]==13:
        
        mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])
        
        rcMuons = []
        rcParticles = []
        for i in range(len(tree.rctyp)):
            p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
            rcParticles.append(p)
            if p.typ == 13:
                rcMuons.append(p)
    
        rcJets = []
        for i in range(len(tree.jene)):
            p = TaggedJet(i,tree.jmas[i],tree.jcha[i],tree.jmox[i],tree.jmoy[i],tree.jmoz[i],tree.jene[i], tree.btag[i], tree.ctag[i])
            rcJets.append(p)

        for muon in rcMuons:
            for photon in rcParticles:
                if photon.typ == 22:
                    thetaDifference = photon.dtheta(muon)
                    phiDifference = photon.dphi(muon)
                    if abs(thetaDifference) < dtheta1:
                        if abs(phiDifference) < dphi1:
                            muon.p += photon.p
                        else:
                            if abs(thetaDifference) < dtheta2:
                                if phiDifference > dphi2Min and phiDifference < dphi2Max:
                                    muon.p += photon.p
            rcParticles[muon.num] = muon

            distance = -1
            invMass = -1
            minAngle = numpy.pi
            for i in range(len(rcJets)):
                angle = rcJets[i].angle(muon)
                if angle < minAngle:
                    minAngle = angle
                    distance = Distance(muon,rcJets[i])
                    invMass = invariantMass(muon, rcJets[i])
            hDistanceToClosestJet.Fill(distance)
            hMassWithClosestJet.Fill(invMass)

                            
    j = j+1

savingFile=TFile('./distanceClosestJet.root',"RECREATE")
hDistanceToClosestJet.Write()
hMassWithClosestJet.Write()
savingFile.Close()
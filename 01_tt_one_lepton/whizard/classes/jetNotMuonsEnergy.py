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

hNotMuonJetEnergy = TH1F("notMuonJetEnergy","Energy of non muon-tagged jets",300,0.,100.)

for event in tree:
    if tree.mcpdg[10]==13:
        
        rcMuons = []
        for i in range(len(tree.rctyp)):
            if tree.rctyp[i] == 13:
                p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
                rcMuons.append(p)
    
        rcJets = []
        for i in range(len(tree.jene)):
            p = TaggedJet(i,tree.jmas[i],tree.jcha[i],tree.jmox[i],tree.jmoy[i],tree.jmoz[i],tree.jene[i], tree.btag[i], tree.ctag[i])
            rcJets.append(p)

        # photon recovery
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
        
        for jet in rcJets:
            minInvMass = -1
            for muon in rcMuons:
                invMass = InvariantMass(muon,jet)
                if invMass < minInvMass or minInvMass == -1:
                    minInvMass = invMass
            if minInvMass > 11:
                hNotMuonJetEnergy.Fill(jet.energy())

savingFile=TFile('./jetNotMuonsEnergy.root',"RECREATE")
hNotMuonJetEnergy.Write()
savingFile.Close()
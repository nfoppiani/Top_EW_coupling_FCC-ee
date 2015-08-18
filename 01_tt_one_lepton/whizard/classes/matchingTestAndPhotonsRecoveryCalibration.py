from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

tree = TChain("MyLCTuple")

tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')
#tree.Add('./../whizard_negMuTau_yyxylv/000/yyxylv_o_*.root')
#tree.Add('./../whizard_negMuTau_yyxylv/001/yyxylv_o_*.root')

dthetaDegrees = 15.
dphiDegrees = 25.

dtheta = numpy.radians(dthetaDegrees)
dphi = numpy.radians(dphiDegrees)

hEnergyDifference = TH1F("energyDifference","Energy matched - energy montecarlo",500,-60.,60.)
hAngle = TH1F("angle","Angle matched-montecarlo",90,0.,4.5)
hDistance = TH1F("distance","Distance between matched and montecarlo muon",300,0.,100.)
hPhotonDistributionW = TH2F("photonDistributionW", "Emitted photons distribution", 1000,dthetaDegrees, dthetaDegrees, 500, -dphiDegrees, dphiDegrees)
hPhotonDistributionNotW = TH2F("photonDistributionNotW", "Emitted photons distribution", 1000,dthetaDegrees, dthetaDegrees, 500, -dphiDegrees, dphiDegrees)
hPhotonDistributionWEnergy = TH2F("photonDistributionWPhoton", "Emitted photons distribution weighted on the photons energy", 1000,dthetaDegrees, dthetaDegrees, 500, -dphiDegrees, dphiDegrees)
hPhotonDistributionNotWEnergy = TH2F("photonDistributionNotWPhotonEnergy", "Emitted photons distribution weighted on the photons energy", 1000,dthetaDegrees, dthetaDegrees, 500, -dphiDegrees, dphiDegrees)
hPhotonDistributionWMuonEnergy = TH2F("photonDistributionWMuonEnergy", "Emitted photons distribution weighted on the muons energy", 1000,dthetaDegrees, dthetaDegrees, 500, -dphiDegrees, dphiDegrees)
hPhotonDistributionNotWMuonEnergy = TH2F("photonDistributionNotWMuonEnergy", "Emitted photons distribution weighted on the muons energy", 1000,dthetaDegrees, dthetaDegrees, 500, -dphiDegrees, dphiDegrees)
hPhotonsIn7DegreesWMuons = TH2F("photonsIn7DegreesWMuon", "Number of photons in a 7 degrees cone", 21, 0., 20.)
hPhotonsIn7DegreesNotWMuons = TH2F("photonsIn7DegreesNotWMuon", "Number of photons in a 7 degrees cone", 21, 0., 20.)
hPhotonsIn8DegreesWMuons = TH2F("photonsIn8DegreesWMuon", "Number of photons in a 8 degrees cone", 21, 0., 20.)
hPhotonsIn8DegreesNotWMuons = TH2F("photonsIn8DegreesNotWMuon", "Number of photons in a 8 degrees cone", 21, 0., 20.)
hPhotonsIn9DegreesWMuons = TH2F("photonsIn9DegreesWMuon", "Number of photons in a 9 degrees cone", 21, 0., 20.)
hPhotonsIn9DegreesNotWMuons = TH2F("photonsIn9DegreesNotWMuon", "Number of photons in a 9 degrees cone", 21, 0., 20.)

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
            hEnergyDifference.Fill(matchedMuon.p.E() - mcMuon.p.E())
            hAngle.Fill(numpy.degrees(mcMuon.angle(matchedMuon)))
            hDistance.Fill(Distance(mcMuon, matchedMuon))

            count7 = 0
            count8 = 0
            count9 = 0
            for photon in rcParticles:
                if photon.typ == 22:
                    thetaDifference = photon.dtheta(matchedMuon)
                    if abs(thetaDifference) < dtheta:
                        phiDifference = photon.dphi(matchedMuon)
                        if abs(phiDifference) < dphi:
                            hPhotonDistributionW.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference))
                            hPhotonDistributionWEnergy.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference), photon.energy())
                            hPhotonDistributionWMuonEnergy.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference), matchedMuon.energy())
                angle = photon.angle(matchedMuon)
                if angle < numpy.radians(9):
                    count9 += 1
                    if angle < numpy.radians(8):
                        count8 += 1
                        if angle < numpy.radians(7):
                            count7 += 1
            hPhotonsIn7DegreesWMuons.Fill(count7)
            hPhotonsIn8DegreesWMuons.Fill(count8)
            hPhotonsIn9DegreesWMuons.Fill(count9)
        
        for muon in rcMuons:
            if muon.num != matchNum:
                count7 = 0
                count8 = 0
                count9 = 0
                for photon in rcParticles:
                    if photon.typ == 22:
                        thetaDifference = photon.dtheta(muon)
                        if abs(thetaDifference) < dtheta:
                            phiDifference = photon.dphi(muon)
                            if abs(phiDifference) < dphi:
                                hPhotonDistributionNotW.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference))
                                hPhotonDistributionNotWEnergy.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference), photon.energy())
                                hPhotonDistributionNotWMuonEnergy.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference), muon.energy())
                    angle = photon.angle(muon)
                    if angle < numpy.radians(9):
                        count9 += 1
                        if angle < numpy.radians(8):
                            count8 += 1
                            if angle < numpy.radians(7):
                                count7 += 1
                hPhotonsIn7DegreesNotWMuons.Fill(count7)
                hPhotonsIn8DegreesNotWMuons.Fill(count8)
                hPhotonsIn9DegreesNotWMuons.Fill(count9)

savingFile=TFile('./matchingTestAndPhotonsRecoveryCalibration.root',"RECREATE")
savingFile.cd()
hEnergyDifference.Write()
hAngle.Write()
hDistance.Write()
hPhotonDistributionW.Write()
hPhotonDistributionNotW.Write()
hPhotonDistributionWEnergy.Write()
hPhotonDistributionNotWEnergy.Write()
hPhotonDistributionWMuonEnergy.Write()
hPhotonDistributionNotWMuonEnergy.Write()
hPhotonsIn7DegreesWMuons.Write()
hPhotonsIn7DegreesNotWMuons.Write()
hPhotonsIn8DegreesWMuons.Write()
hPhotonsIn8DegreesNotWMuons.Write()
hPhotonsIn9DegreesWMuons.Write()
hPhotonsIn9DegreesNotWMuons.Write()
savingFile.Close()
from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

tree = TChain("MyLCTuple")

tree.Add('./../whizard_negMuTau_yyxylv/000/yyxylv_o_*.root')
tree.Add('./../whizard_negMuTau_yyxylv/001/yyxylv_o_*.root')

dthetaDegrees = 1.7
dphiDegrees = 6.

dtheta = numpy.radians(dthetaDegrees)
dphi = numpy.radians(dphiDegrees)

hEnergyDifference = TH1F("energyDifference","Energy matched - energy montecarlo",300,-60.,20.)
hAngle = TH1F("angle","Angle matched-montecarlo",100,0.,6.)
hDistance = TH1F("distance","Distance between matched and montecarlo muon",300,0.,100.)
hPhotonDistributionW = TH2F("photonDistributionW", "Emitted photons distribution in theta and phi", 60,dthetaDegrees, dthetaDegrees, 60, -dphiDegrees, dphiDegrees)
hPhotonDistributionNotW = TH2F("photonDistributionNotW", "Emitted photons distribution in theta and phi", 60,dthetaDegrees, dthetaDegrees, 60, -dphiDegrees, dphiDegrees)
hPhotonDistributionWEnergy = TH2F("photonDistributionWPhoton", "Emitted photons distribution in theta and phi", 60,dthetaDegrees, dthetaDegrees, 60, -dphiDegrees, dphiDegrees)
hPhotonDistributionNotWEnergy = TH2F("photonDistributionNotWPhotonEnergy", "Emitted photons distribution in theta and phi", 60,dthetaDegrees, dthetaDegrees, 60, -dphiDegrees, dphiDegrees)
hPhotonDistributionWMuonEnergy = TH2F("photonDistributionWMuonEnergy", "Emitted photons distribution in theta and phi", 60,dthetaDegrees, dthetaDegrees, 60, -dphiDegrees, dphiDegrees)
hPhotonDistributionNotWMuonEnergy = TH2F("photonDistributionNotWMuonEnergy", "Emitted photons distribution in theta and phi", 60,dthetaDegrees, dthetaDegrees, 60, -dphiDegrees, dphiDegrees)

k = 0

for event in tree:
    if k % 990 == 0:
        print 'file ', k/99
    k += 1
    
    if tree.mcpdg[10]==13:
        mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])
        
        rcParticles = []
        for i in range(len(tree.rctyp)):
			p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
			rcParticles.append(p)

        matchNum = mcMuon.matchMuon(rcParticles)
        
        if matchNum != -1 and rcParticles[matchNum].typ == 13:
            matchedMuon = rcParticles[matchNum]
            hEnergyDifference.Fill(matchedMuon.p.E() - mcMuon.p.E())
            hAngle.Fill(numpy.degrees(mcMuon.angle(matchedMuon)))
            hDistance.Fill(Distance(mcMuon, matchedMuon))
            
            for photon in rcParticles:
                if photon.typ == 22:
                    thetaDifference = photon.dtheta(matchedMuon)
                    if abs(thetaDifference) < dtheta:
                        phiDifference = photon.dphi(matchedMuon)
                        if abs(phiDifference) < dphi:
                            hPhotonDistributionW.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference))
                            hPhotonDistributionWEnergy.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference), photon.energy())
                            hPhotonDistributionWMuonEnergy.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference), matchedMuon.energy())
    
        for muon in rcParticles:
            if muon.typ == 13 and muon.num != matchNum:
                for photon in rcParticles:
                    if photon.typ == 22:
                        thetaDifference = photon.dtheta(muon)
                        if abs(thetaDifference) < dtheta:
                            phiDifference = photon.dphi(muon)
                            if abs(phiDifference) < dphi:
                                hPhotonDistributionNotW.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference))
                                hPhotonDistributionNotWEnergy.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference), photon.energy())
                                hPhotonDistributionNotWMuonEnergy.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference), muon.energy())

savingFile=TFile('./matchingTestAndFindPhotonsEnergy.root',"RECREATE")
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
savingFile.Close()
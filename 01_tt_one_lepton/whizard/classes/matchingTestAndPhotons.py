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

hEnergyDifference = TH1F("energyDifference","Energy matched - energy montecarlo",100,-60.,20.)
hAngle = TH1F("angle","Angle matched-montecarlo",80,0.,10.)
hDistance = TH1F("distance","Distance between matched and montecarlo muon",100,0.,100.)
hPhotonDistribution = TH2F("photonDistribution", "Emitted photons distribution in theta and phi", 20, -1.2*dthetaDegrees, 1.2*dthetaDegrees, 20, -dphiDegrees, dphiDegrees)

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
                            hPhotonDistribution.Fill(numpy.degrees(thetaDifference), numpy.degrees(phiDifference))

savingFile=TFile('./matchingTestAndPhotons.root',"RECREATE")
savingFile.cd()
hEnergyDifference.Write()
hAngle.Write()
hDistance.Write()
hPhotonDistribution.Write()
savingFile.Close()
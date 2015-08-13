from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')

dtheta = 0.03
dphi = 0.1

hEnergyDifference = TH1F("Energy matched - energy montecarlo","Energy matched - energy montecarlo",100,-50.,50.)
hTheta = TH1F("Theta matched,montecarlo","Theta matched,montecarlo",200,-0.2,0.2)
hDistance = TH1F("Distance between matched and montecarlo muon","Distance between matched and montecarlo muon",100,0.,100.)
hPhotonDistribution = TH2F("photonDistribution", "Emitted photons distribution in theta and phi", 20, -2*dtheta, 2*dtheta, 20, -dphi, dphi)

#hType=TH1F("type of closest particle","type of closest particle",50000,-250,3000)

for event in tree:
    if tree.mcpdg[10]==13:
        mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])

        rcParticles = []
        for i in range(len(tree.rctyp)):
			p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
			rcParticles.append(p)

        matchNum = mcMuon.matchMuon(rcParticles)
        if matchNum != -1 and rcParticles[matchNum].type == 13:
            
            hEnergyDifference.Fill(rcParticles[matchNum].p.E() - mcMuon.p.E())
            hTheta.Fill(mcMuon.angle(rcParticles[matchNum]))
            hDistance.Fill(Distance(mcMuon, rcParticles[matchNum]))
        #else:
            #for part in rcParticles:
            part = rcParticles[matchNum]
                #if part.type == 13:
            for photon in rcParticles:
                if photon.type == 22:
                    thetaMuon = part.theta()
                    thetaPhoton = photon.theta()
                    if abs(thetaMuon-thetaPhoton) < dtheta:
                        phiMuon = part.phi()
                        phiPhoton = photon.phi()
                        phiDifference = phiPhoton-phiMuon
                        if phiDifference > numpy.pi:
                            phiDifference -= 2*numpy.pi
                        else:
                            if phiDifference < -numpy.pi:
                                phiDifference += 2*numpy.pi
                        if abs(phiDifference) < dphi:
                            hPhotonDistribution.Fill(thetaMuon-thetaPhoton, phiDifference)
		
		#hType.Fill(rcParticles[MatchNum].type)

savingFile=TFile('./../plot/matchingTestMuons.root',"RECREATE")
savingFile.cd()
hEnergyDifference.Write()
hTheta.Write()
hDistance.Write()
hPhotonDistribution.Write()
#hType.Write()
savingFile.Close()
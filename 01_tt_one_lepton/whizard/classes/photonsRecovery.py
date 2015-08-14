from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

tree = TChain("MyLCTuple")

#tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')
tree.Add('./../whizard_negMuTau_yyxylv/000/yyxylv_o_*.root')
tree.Add('./../whizard_negMuTau_yyxylv/001/yyxylv_o_*.root')

dtheta1Degrees = 0.4
dphi1Degrees = 0.2
dtheta2Degrees = 0.27
dphi2DegreesMax = 2.7
dphi2DegreesMin = -0.2

dtheta1 = numpy.radians(dtheta1Degrees)
dphi1 = numpy.radians(dphi1Degrees)
dtheta2 = numpy.radians(dtheta2Degrees)
dphi2Max = numpy.radians(dphi2DegreesMax)
dphi2Min = numpy.radians(dphi2DegreesMin)

hBefore = TH1F("energyDifferenceBefore","Energy matched - energy montecarlo before recovery",300,-60.,60.)
hAfter = TH1F("energyDifferenceAfter","Energy matched - energy montecarlo after recovery",300,-60.,60.)

k = 0

for event in tree:
    if k % 990 == 0:
        print 'file ', k/99
    if tree.mcpdg[10]==13:
        #print 'EVENT ', k
        mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])
        #print 'MC', '\t', mcMuon.energy(), '\t', mcMuon.px(), '\t', mcMuon.py(), '\t', mcMuon.pz()
        
        rcParticles = []
        for i in range(len(tree.rctyp)):
			p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
			rcParticles.append(p)

        matchNum = mcMuon.matchMuon(rcParticles)
    
        for muon in rcParticles:
            if muon.typ == 13:
                if muon.num == matchNum:
                    hBefore.Fill(muon.energy() - mcMuon.energy())
                    #print 'RC', '\t', muon.energy(), '\t', muon.px(), '\t', muon.py(), '\t', muon.pz()
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
                                #if muon.num == matchNum:
                                    #print 'RC', '\t', muon.energy(), '\t', muon.px(), '\t', muon.py(), '\t', muon.pz()
                if muon.num == matchNum:
                    hAfter.Fill(muon.energy() - mcMuon.energy())
        # print
    k += 1

savingFile=TFile('./photonsRecovery.root',"RECREATE")
hBefore.Write()
hAfter.Write()
savingFile.Close()
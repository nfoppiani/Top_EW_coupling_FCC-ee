from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain, THStack
import numpy
from particleClass import *

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')

#declaration of histograms

sPtClosestJet = THStack("ptClosestJet","Pt to the closest Jet")
hPtSignal = TH1F("ptClosestJetSignal","Pt to the closest Jet - signal",100,0.,100.)
hPtBackground = TH1F("ptClosestJetBackground","Pt to the closest Jet - background",100,0.,100.)

sAngleClosestCharge = THStack("angleClosestCharge","Angle to the closest charged particle")
hAngleChargeSignal = TH1F("angleClosestChargeSignal","Angle to the closest charged particle - signal",100,0.,90.)
hAngleChargeBackground = TH1F("angleClosestChargeBackground","Angle to the closest charged particle - background",100,0.,90.)

sEnergyInCone = THStack("energyInCone","Energy in a cone of 10 degrees")
hEnergyInConeSignal = TH1F("energyInConeSignal","Energy in a cone of 10 degrees - signal",100,0.,60.)
hEnergyInConeBackground = TH1F("energyInConeBackground","Energy in a cone of 10 degrees - background",100,0.,60.)

#loop on the events
for event in tree:
    if tree.mcpdg[10]==13:
        mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])
        rcParticles = []
        for i in range(len(tree.rctyp)):
            p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
            rcParticles.append(p)
        rcJets = []
        for i in range(len(tree.jene)):
			p = Jet(i,tree.jmas[i],tree.jmox[i],tree.jmoy[i],tree.jmoz[i],tree.jene[i])
			rcJets.append(p)

        rcMatchNum = mcMuon.matchMuon(rcParticles)      # RC matched muon progressive number in rcParticles
        
        if rcMatchNum != -1:
    
            pt = rcParticles[rcMatchNum].ptToClosestJet(rcJets)
            hPtSignal.Fill(pt)
            
            angle = rcParticles[rcMatchNum].angleToClosestCharge(rcParticles)
            hAngleChargeSignal.Fill(numpy.degrees(angle))
        
            energy = rcParticles[rcMatchNum].energyInCone(rcParticles)
            hEnergyInConeSignal.Fill(energy)
            
        for part in rcParticles:
            if part.type == 13 and part.num != rcMatchNum:
                
                pt = part.ptToClosestJet(rcJets)
                hPtBackground.Fill(pt)
                    
                angle = part.angleToClosestCharge(rcParticles)
                hAngleChargeBackground.Fill(numpy.degrees(angle))

                energy = part.energyInCone(rcParticles)
                hEnergyInConeBackground.Fill(energy)

savingFile=TFile('./backgroundToSignalMuon2.root',"RECREATE")

hPtSignal.Write()
hPtBackground.Write()

hAngleChargeSignal.Write()
hAngleChargeBackground.Write()

hEnergyInConeSignal.Write()
hEnergyInConeBackground.Write()

hPtSignal.SetLineColor(2)
hPtBackground.SetLineColor(3)
sPtClosestJet.Add(hPtSignal)
sPtClosestJet.Add(hPtBackground)
sPtClosestJet.Write()

hAngleChargeSignal.SetLineColor(2)
hAngleChargeBackground.SetLineColor(3)
sAngleClosestCharge.Add(hAngleChargeSignal)
sAngleClosestCharge.Add(hAngleChargeBackground)
sAngleClosestCharge.Write()

hEnergyInConeSignal.SetLineColor(2)
hEnergyInConeBackground.SetLineColor(3)
sEnergyInCone.Add(hEnergyInConeSignal)
sEnergyInCone.Add(hEnergyInConeBackground)
sEnergyInCone.Write()

savingFile.Close()
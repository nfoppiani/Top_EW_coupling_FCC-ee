from ROOT import TFile, TTree, TLorentzVector, TH1F, TH2F, TChain, THStack, TGraph, TCanvas
import numpy
import string
from particleClass import *

generatedMuons=69397.

rcMuonFile=TFile("./../tree/negMuonsRcTreeTry100files.root","OPEN")
rcMuonTree = rcMuonFile.Get("negMuonsRC")

savingFile =TFile("./../plot/compareIsolationAlgorithm.root","RECREATE")

def makeRedGreenHisto(tree,name,nBins,min,max,variable,option1,option2,save):

    hTot=THStack(name,name)

    hPartial1=TH1F("pt1","pt1",nBins,min,max)
    tree.Project("pt1",variable,option1)
    hPartial2=TH1F("pt2","pt2",nBins,min,max)
    tree.Project("pt2",variable,option2)

    hPartial1.SetFillColor(2) #set the red fill color
    hTot.Add(hPartial1)

    hPartial2.SetFillColor(3) #set the green fill color
    hTot.Add(hPartial2)

    save.cd()
    hTot.Write()
    return

#pt to closest Jet
makeRedGreenHisto(rcMuonTree,"ptToClosestJet",200,0.,80.,"rcPtToClosestJet","rcMuMatch==1","rcMuMatch==0",savingFile)

#rcAngleClosestCharge
makeRedGreenHisto(rcMuonTree,"rcAngleClosestCharge",200,0.,2.,"rcAngleClosestCharge","rcMuMatch==1","rcMuMatch==0",savingFile)

#rcAngleClosestChargeOrNeutron
makeRedGreenHisto(rcMuonTree,"rcAngleClosestChargeOrNeutron",200,0.,2.,"rcAngleClosestChargeOrNeutron","rcMuMatch==1","rcMuMatch==0",savingFile)

#rcAngleToClosestParticleNotPhoton
makeRedGreenHisto(rcMuonTree,"rcAngleToClosestParticleNotPhoton",200,0.,2.,"rcAngleToClosestParticleNotPhoton","rcMuMatch==1","rcMuMatch==0",savingFile)

#rcEnergyInCone
makeRedGreenHisto(rcMuonTree,"rcEnergyInCone",200,0.,80.,"rcEnergyInCone","rcMuMatch==1","rcMuMatch==0",savingFile)

#rcEnergyChargeInCone
makeRedGreenHisto(rcMuonTree,"rcEnergyChargeInCone",200,0.,80.,"rcEnergyChargeInCone","rcMuMatch==1","rcMuMatch==0",savingFile)

#rcEnergyInConeWithoutPhotons
makeRedGreenHisto(rcMuonTree,"rcEnergyInConeWithoutPhotons",200,0.,80.,"rcEnergyInConeWithoutPhotons","rcMuMatch==1","rcMuMatch==0",savingFile)

#rcEnergyChargeInConeNorm
makeRedGreenHisto(rcMuonTree,"rcEnergyChargeInConeNorm",200,0.,80.,"rcEnergyChargeInConeNorm","rcMuMatch==1","rcMuMatch==0",savingFile)

savingFile.Close()

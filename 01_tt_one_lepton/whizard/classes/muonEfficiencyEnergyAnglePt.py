from ROOT import TFile, TTree, TLorentzVector, TH1F, TH2F, TChain, THStack, TGraph, TCanvas
import numpy
from particleClass import *

#saving file
savingFile=TFile("./../plot/negMuonsRcEfficiencyEnergyAnglePt.root","RECREATE")

#tree reconstructed muons file
rcMuonFile=TFile("./../tree/rcTree/negMuonsRcTree.root","OPEN")
rcMuonTree = rcMuonFile.Get("negMuonsRC")

#best cut variables
pTMax=4.
energyMin=6.
angleMax=0.35

#histogram montecarlo electrons
mcMuonFile=TFile("./../ntuple/leptons_tree/negative_muons_tree.root","OPEN")
mcMuonTree = mcMuonFile.Get("negative_muons_tree")

mcNumberoOfMuons=mcMuonTree.GetEntries()

#efficiency in measuring energy and angle

#mc
mcEnergyAngleDistribution=TH2F("mcMuonsEnergyAngleDistribution","Montecarlo Energy Angle Distribution",40,0.,1.,40,-1.,1.)
mcMuonTree.Project("mcMuonsEnergyAngleDistribution","mcCosTheta:mcRedEne")

savingFile.cd()
mcEnergyAngleDistribution.Write()

#rc
rcEnergyAngleDistribution=TH2F("rcMuonsEnergyAngleDistribution","Reconstructed muons Energy Angle Distribution",40,0.,1.,40,-1.,1.)
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcMuonsEnergyAngleDistribution","rcMuCosTheta:rcMuRedEne",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

savingFile.cd()
rcEnergyAngleDistribution.Write()

#ratio
ratioRcMcEnergyAngleDistribution=TH2F("ratioRcMcEnergyAngleDistribution","Ratio MC/REC muons Energy Angle Distribution",40,0.,1.,40,-1.,1.)
ratioRcMcEnergyAngleDistribution.Add(rcEnergyAngleDistribution)
ratioRcMcEnergyAngleDistribution.Divide(mcEnergyAngleDistribution)

savingFile.cd()
ratioRcMcEnergyAngleDistribution.Write()

#only cos theta
mcAngleDistribution=TH1F("mcMuonsAngleDistribution","Montecarlo Angle Distribution",400,-1.,1.)
mcMuonTree.Project("mcMuonsAngleDistribution","mcCosTheta")

rcAngleDistribution=TH1F("rcMuonsAngleDistribution","Reconstructed muons Angle Distribution",400,-1.,1.)
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcMuonsAngleDistribution","rcMuCosTheta",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

ratioRcMcAngleDistribution=TH1F("ratioRcMcAngleDistribution","Ratio MC/REC muons Angle Distribution",400,-1.,1.)
ratioRcMcAngleDistribution.Add(rcAngleDistribution)
ratioRcMcAngleDistribution.Divide(mcAngleDistribution)

savingFile.cd()
ratioRcMcAngleDistribution.Write()

#only energy
mcEnergyDistribution=TH1F("mcMuonsEnergyDistribution","Montecarlo Energy Distribution",400,-1.,1.)
mcMuonTree.Project("mcMuonsEnergyDistribution","mcCosTheta")

rcEnergyDistribution=TH1F("rcMuonsEnergyDistribution","Reconstructed muons Energy Distribution",400,-1.,1.)
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcMuonsEnergyDistribution","rcMuCosTheta",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

ratioRcMcEnergyDistribution=TH1F("ratioRcMcEnergyDistribution","Ratio MC/REC muons Energy Distribution",400,-1.,1.)
ratioRcMcEnergyDistribution.Add(rcEnergyDistribution)
ratioRcMcEnergyDistribution.Divide(mcEnergyDistribution)

savingFile.cd()
ratioRcMcEnergyDistribution.Write()

#efficiency in 1/PT

#delta 1/pt vs cosTheta
rcDeltaOneOverPtVSCosTheta=TH2F("rcDeltaOneOverPtVSCosTheta","Delta 1/pt in function of cosTheta",400,-1.,1.,400,-0.01,0.01)
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcDeltaOneOverPtVSCosTheta","rcMuDeltaOneOverPt:rcMuCosTheta",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

savingFile.cd()
rcDeltaOneOverPtVSCosTheta.Write()

#delta 1/pt vs Energy
rcDeltaOneOverPtVSEnergy=TH2F("rcDeltaOneOverPtVSEnergy","Delta 1/pt in function of Energy",400,0.,1.,5000,-0.1,2)
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcDeltaOneOverPtVSEnergy","rcMuDeltaOneOverPt:rcMuRedEne",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

savingFile.cd()
rcDeltaOneOverPtVSEnergy.Write()

#delta Alpha vs cosTheta

rcDeltaAlphaVSCosTheta=TH2F("rcDeltaAlphaVSCosTheta","Delta Alpha in function of cosTheta",400,-1.,1.,400,0.,1.)
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcDeltaAlphaVSCosTheta","rcMuDeltaAlpha:rcMuCosTheta",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

savingFile.cd()
rcDeltaAlphaVSCosTheta.Write()



#delta Alpha vs PT
rcDeltaAlphaVSPt=TH2F("rcDeltaAlphaVSPt","Delta Alpha in function of Pt",400,10,120,500,0.,1.)
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcDeltaAlphaVSPt","rcMuDeltaAlpha:rcMuPt",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

savingFile.cd()
rcDeltaAlphaVSPt.Write()


savingFile.Close()

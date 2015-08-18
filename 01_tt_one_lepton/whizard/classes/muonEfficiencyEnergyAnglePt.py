from ROOT import TFile, TTree, TLorentzVector, TH1F, TH2F, TChain, THStack, TGraph, TCanvas, TProfile, TGraphErrors, TF1
import numpy
from particleClass import *


def fitSliceGaus(h2,nBin,max,title,save):

    means=numpy.zeros(nBin)
    sigmas=numpy.zeros(nBin)

    x=numpy.zeros(nBin)
    ex=numpy.zeros(nBin)

    binWidth=h2.GetXaxis().GetBinWidth(1)

    for i in range(nBin):
        #"projection {i}".format(i=i+1)
        h1=h2.ProjectionY("",i+1,i+1)
        h1.Fit("gaus")
        gaus = TF1(h1.GetFunction("gaus"))
        h1.Fit("gaus","","",(gaus.GetParameter(1))-2.*(gaus.GetParameter(2)),max)
        gaus = h1.GetFunction("gaus")
        h1.Fit("gaus","","",(gaus.GetParameter(1))-2.*(gaus.GetParameter(2)),max)
        gaus = h1.GetFunction("gaus")
        h1.Fit("gaus","","",(gaus.GetParameter(1))-2.*(gaus.GetParameter(2)),max)
        gaus = h1.GetFunction("gaus")
        h1.Fit("gaus","","",(gaus.GetParameter(1))-2.*(gaus.GetParameter(2)),max)
        gaus = h1.GetFunction("gaus")
        h1.Fit("gaus","","",(gaus.GetParameter(1))-2.*(gaus.GetParameter(2)),max)
        gaus = h1.GetFunction("gaus")

        means[i]=gaus.GetParameter(1)
        sigmas[i]=gaus.GetParameter(2)#/(1.+min(0.,gaus.GetParameter(1)))
        x[i]=binWidth*(i+0.5)
        ex[i]=0.

    graph= TGraphErrors(len(means),x,means,ex,sigmas)
    graph.SetTitle(title)

    save.cd()
    graph.Write()

    return

#saving file
savingFile=TFile("./../plot/negMuonsRcEfficiencyEnergyAnglePt.root","RECREATE")

#tree reconstructed muons file
rcMuonFile=TFile("./../tree/negMuonsRcTreeTryAllfiles.root","OPEN")
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

ratioRcMcAngleDistribution=TH1F("ratioRcMcAngleDistribution","Ratio REC/MC muons Angle Distribution",400,-1.,1.)
ratioRcMcAngleDistribution.Add(rcAngleDistribution)
ratioRcMcAngleDistribution.Divide(mcAngleDistribution)

savingFile.cd()
ratioRcMcAngleDistribution.Write()

#only energy
mcEnergyDistribution=TH1F("mcMuonsEnergyDistribution","Montecarlo Energy Distribution",400,0.,1.)
mcMuonTree.Project("mcMuonsEnergyDistribution","mcRedEne")

rcEnergyDistribution=TH1F("rcMuonsEnergyDistribution","Reconstructed muons Energy Distribution",400,0.,1.)
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcMuonsEnergyDistribution","rcMuRedEne",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

ratioRcMcEnergyDistribution=TH1F("ratioRcMcEnergyDistribution","Ratio REC/MC muons Energy Distribution",400,0.,1.)
ratioRcMcEnergyDistribution.Add(rcEnergyDistribution)
ratioRcMcEnergyDistribution.Divide(mcEnergyDistribution)

savingFile.cd()
ratioRcMcEnergyDistribution.Write()

#efficiency in 1/PT

#delta 1/pt vs cosTheta
# rcDeltaOneOverPtVSCosTheta=TH2F("rcDeltaOneOverPtVSCosTheta","Delta 1/pt in function of cosTheta",400,-1.,1.,400,-0.01,0.01)
# cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
# rcMuonTree.Project("rcDeltaOneOverPtVSCosTheta","rcMuDeltaOneOverPt:rcMuCosTheta",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))
#
# savingFile.cd()
# rcDeltaOneOverPtVSCosTheta.Write()
#
# #delta 1/pt vs Energy
# rcDeltaOneOverPtVSEnergy=TH2F("rcDeltaOneOverPtVSEnergy","Delta 1/pt in function of Energy",400,0.,1.,5000,-0.1,2)
# cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
# rcMuonTree.Project("rcDeltaOneOverPtVSEnergy","rcMuDeltaOneOverPt:rcMuRedEne",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))
#
# savingFile.cd()
# rcDeltaOneOverPtVSEnergy.Write()
#
# #delta Alpha vs cosTheta
#
# rcDeltaAlphaVSCosTheta=TH2F("rcDeltaAlphaVSCosTheta","Delta Alpha in function of cosTheta",400,-1.,1.,400,0.,1.)
# cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
# rcMuonTree.Project("rcDeltaAlphaVSCosTheta","rcMuDeltaAlpha:rcMuCosTheta",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))
#
# savingFile.cd()
# rcDeltaAlphaVSCosTheta.Write()
#
#
#
# #delta Alpha vs PT
# rcDeltaAlphaVSPt=TH2F("rcDeltaAlphaVSPt","Delta Alpha in function of Pt",400,10,120,500,0.,1.)
# cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
# rcMuonTree.Project("rcDeltaAlphaVSPt","rcMuDeltaAlpha:rcMuPt",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))
#
# savingFile.cd()
# rcDeltaAlphaVSPt.Write()

#delta 1/pt vs CosTheta
rcDeltaOneOverPtVSCosTheta=TProfile("rcDeltaOneOverPtVSCosTheta","Delta 1/pt in function of cosTheta",25,-1.,1.,"s")
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcDeltaOneOverPtVSCosTheta","rcMuDeltaOneOverPt:rcMuCosTheta",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

savingFile.cd()
rcDeltaOneOverPtVSCosTheta.Write()

# 
# rcDeltaOneOverPtVSCosTheta=TH2F("rcDeltaOneOverPtVSCosTheta","Delta 1/pt in function of CosTheta",25,-1.,1.,1000,-0.5,0.5)
# cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
# rcMuonTree.Project("rcDeltaOneOverPtVSCosTheta","rcMuDeltaOneOverPt:rcMuCosTheta",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))
#
# fitSliceGaus(rcDeltaOneOverPtVSCosTheta,25,0.5,"rcDeltaOneOverPtVSCosTheta",savingFile)
#

#delta 1/pt vs Energy
rcDeltaOneOverPtVSEnergy=TProfile("rcDeltaOneOverPtVSEnergy","Delta 1/pt in function of Energy",25,0.,1.,"s")
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcDeltaOneOverPtVSEnergy","rcMuDeltaOneOverPt:rcMuRedEne",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

savingFile.cd()
rcDeltaOneOverPtVSEnergy.Write()


rcDeltaOneOverPtVSEnergy=TH2F("rcDeltaOneOverPtVSEnergy","Delta 1/pt in function of Energy",15,0.,1.,1000,-0.5,0.5)
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcDeltaOneOverPtVSEnergy","rcMuDeltaOneOverPt:rcMuRedEne",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

fitSliceGaus(rcDeltaOneOverPtVSEnergy,15,0.5,"rcDeltaOneOverPtVSEnergy",savingFile)

#delta Theta vs cosTheta

rcDeltaThetaVSCosTheta=TProfile("rcDeltaThetaVSCosTheta","Delta Theta in function of cosTheta",18,-1.,1.,"s")
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcDeltaThetaVSCosTheta","rcMuDeltaTheta:rcMuCosTheta",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

savingFile.cd()
rcDeltaThetaVSCosTheta.Write()

#delta Theta vs PT
rcDeltaThetaVSPt=TProfile("rcDeltaThetaVSPt","Delta Theta in function of Pt",18,10,120,"s")
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcDeltaThetaVSPt","rcMuDeltaTheta:rcMuPt",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

savingFile.cd()
rcDeltaThetaVSPt.Write()

#delta Phi vs cosTheta

rcDeltaPhiVSCosTheta=TProfile("rcDeltaPhiVSCosTheta","Delta Phi in function of cosTheta",18,-1.,1.,"s")
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcDeltaPhiVSCosTheta","rcMuDeltaPhi:rcMuCosTheta",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

savingFile.cd()
rcDeltaPhiVSCosTheta.Write()

#delta Phi vs PT
rcDeltaPhiVSPt=TProfile("rcDeltaPhiVSPt","Delta Phi in function of Pt",18,10,120,"s")
cutString="rcEnergyInCone<{energyMin} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}"
rcMuonTree.Project("rcDeltaPhiVSPt","rcMuDeltaPhi:rcMuPt",cutString.format(pTMax=pTMax,angleMax=angleMax,energyMin=energyMin))

savingFile.cd()
rcDeltaPhiVSPt.Write()




savingFile.Close()

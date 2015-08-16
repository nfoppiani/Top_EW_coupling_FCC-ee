from ROOT import TFile, TTree, TLorentzVector, TH1F, TH2F, TChain, THStack, TGraph, TCanvas
import numpy
import string
from particleClass import *

generatedMuons=69397.

rcMuonFile=TFile("./../tree/rcTree/negMuonsRcTree.root","OPEN")
rcMuonTree = rcMuonFile.Get("negMuonsRC")

#this script calculates the efficiency and purity with cut

#definition of area

#pTMax=4.
#energyMin=2.
#angleMax=numpy.array([0.2,0.25,0.3,0.35,0.40,0.45,0.50,0.55,0.60,0.65])

pTMax=4.

energyMin=numpy.array([1.5,2.0,2.5,2.8,3.,3.5,4.,5.,6.,7.])
angleMax=0.35



matched=numpy.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])
nonMatched=numpy.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])

efficiency=numpy.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])
purity=numpy.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])
prod=numpy.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])
for i in range(len(energyMin)):
    matchString= "(rcEnergyInCone<{energyMini} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}) && rcMuMatch==1"
    matched[i]=rcMuonTree.GetEntries(matchString.format(pTMax=pTMax,angleMax=angleMax,energyMini=energyMin[i]))

    nonMatchString= "(rcEnergyInCone<{energyMini} || rcPtToClosestJet>{pTMax} || rcAngleClosestCharge>{angleMax}) && rcMuMatch==0"
    nonMatched[i]=rcMuonTree.GetEntries(nonMatchString.format(pTMax=pTMax,angleMax=angleMax,energyMini=energyMin[i]))
    print "energyMin",i, energyMin[i]
    efficiency[i] = matched[i] /generatedMuons
    print "efficiency",i, efficiency[i]
    if (matched[i]+nonMatched[i])>0:
        purity[i]=1-(nonMatched[i]/(matched[i]+nonMatched[i]))
        print "purity",i, purity[i]
    prod[i]=efficiency[i]*purity[i]

Eff=TGraph(len(energyMin),energyMin,efficiency)
Pur=TGraph(len(energyMin),energyMin,purity)

ROC=TGraph(len(efficiency),efficiency,purity)
ROC.SetTitle("ROC function varying the energy min of the cut")
ROC.GetXaxis().SetTitle("Efficiency")
ROC.GetYaxis().SetTitle("Purity")
ROC.GetXaxis().CenterTitle()
ROC.GetYaxis().CenterTitle()
ROC.SetMarkerColor(4)

c1=TCanvas("ROC function varying the energy min of the cut","ROC function varying the energy min of the cut",800,800)
c1.SetGrid()
c1.cd()
ROC.Draw("AC*")

product=TGraph(len(efficiency),energyMin,prod)
product.SetTitle("Efficiency times purity varying the energy min of the cut")
product.GetXaxis().SetTitle("Energy min of the cut")
product.GetYaxis().SetTitle("Efficiency times purity")
product.GetXaxis().CenterTitle()
product.GetYaxis().CenterTitle()
product.SetMarkerColor(4)

c2=TCanvas("Efficiency times purity varying the energy min of the cut","Efficiency times purity varying the energy min of the cut",800,800)
c2.SetGrid()
c2.cd()
product.Draw("AC*")

from ROOT import TFile, TTree, TChain, TCanvas, TH1, TH2, TH3
import numpy

myfile=TFile("../ntuple/leptons_tree/negative_muons_tree.root","OPEN")

mytree=myfile.Get("negative_muons_tree")

mcMuonEnAngleDistribution=TH2F("Mc muons energy-angle distribution","Mc muons energy-angle distribution", 30,0.,1.,30,-1.,1.)

for event in mytree:

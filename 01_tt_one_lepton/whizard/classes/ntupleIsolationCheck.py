from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *

tree = TChain("MyLCTuple")

#tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')
tree.Add('./../whizard_negMuTau_yyxylv/000/yyxylv_o_*.root')
tree.Add('./../whizard_negMuTau_yyxylv/001/yyxylv_o_*.root')

hNIsoMu = TH1F("nIsoMu", "Number of isolated particles", 10, 0., 9.)
hNIsoTau = TH1F("nIsoTau", "Number of isolated particles", 10, 0., 9.)

k = 0

for event in tree:
    if k % 990 == 0:
        print 'file ', k/99
    k += 1
    
    if tree.mcpdg[10]==13:
        hNIsoMu.Fill(tree.niso)
    else:
        if tree.mcpdg[10]==15:
            hNIsoTau.Fill(tree.niso)

savingFile=TFile('./ntupleIsolationCheck.root',"RECREATE")
savingFile.cd()
hNIsoMu.Write()
hNIsoTau.Write()
savingFile.Close()
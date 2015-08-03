from ROOT import TFile, TTree, TH2F
import numpy
import glob

file = TFile.Open("../ntuple/electrons_Tree.root")
tree = file.Get("electrons_Tree")

h_mc=TH2F("mc_electrons","mc_electrons",200,0.112426,1.,200,-1.,1.)


for event in tree:
	h_mc.Fill(tree.mcRedEne,tree.mcCosTheta)


savingFile = TFile("../plot/electrons_histo.root", "CREATE")

savingFile.cd()
h_mc.Write()      
savingFile.Close()

h_mc.Draw()

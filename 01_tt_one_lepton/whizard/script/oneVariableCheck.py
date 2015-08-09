from ROOT import TFile, TH2F, TH1F
import numpy

# A_MIN SETTING
a = -0.015

# getting the analytic histograms

myfile_an = TFile("../analytic/SMCrossWhizard364.root","READ")

h_S0 = myfile_an.Get("smcross")
h_f1 = myfile_an.Get("FBzed")

#getting the montecarlo histogram

myfile_mc = TFile("../plot/2dWhizardLeptons200Histo.root","READ")
electronHisto = myfile_mc.Get("electronReducedEnergyAndAngleHisto")

electronHisto.Scale(1/electronHisto.Integral())
h_f1.Scale(a)
h_S0.Add(h_f1)
h_S0.Scale(1/h_S0.Integral())

savingFile = TFile("../plot/oneVariableCheck.root", "CREATE")

BSMhisto = h_S0.ProjectionY()
BSMhisto.Scale(1/BSMhisto.Integral())
SMhisto = electronHisto.ProjectionY()
SMhisto.Scale(1/SMhisto.Integral())

BSMhisto.SetNameTitle("cosThetaBSMprojection", "Cos(theta) BSM projection")
SMhisto.SetNameTitle("cosThetaSMprojection", "Cos(theta) SM projection")
BSMhisto.Write()
SMhisto.Write()

BSMhisto1 = h_S0.ProjectionX()
BSMhisto1.Scale(1/BSMhisto1.Integral())
SMhisto1 = electronHisto.ProjectionX()
SMhisto1.Scale(1/SMhisto1.Integral())
BSMhisto1.SetNameTitle("xBSMprojection", "x BSM projection")
SMhisto1.SetNameTitle("xSMprojection", "x SM projection")
BSMhisto1.Write()
SMhisto1.Write()

savingFile.Close()

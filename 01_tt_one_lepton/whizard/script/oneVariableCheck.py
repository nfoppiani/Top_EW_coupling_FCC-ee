from ROOT import TFile, TH2F, TH1F
import numpy

# A_MIN SETTING
a = -0.015

# getting the analytic histograms

myfile_an = TFile("SMCrossWhizard365.root","READ")

h_S0 = myfile_an.Get("smcross")
h_f1 = myfile_an.Get("FBzed")

#getting the montecarlo histogram

myfile_mc = TFile("2dWhizardLeptons200Histo.root","READ")
electronHisto = myfile_mc.Get("electronReducedEnergyAndAngleHisto")

electronHisto.Scale(1/electronHisto.Integral()
h_f1.Scale(a)
h_S0.Add(h_f1)
h_S0.Scale(1/h_S0.Integral()

savingFile = TFile("./oneVariableCheck.root", "CREATE")

BSMhisto = h_S0.ProjectionY()
SMhisto = electronHisto.ProjectionY()
BSMhisto.SetNameTitle("cosThetaBSMprojection", "Cos(theta) BSM projection")
SMhisto.SetNameTitle("cosThetaSMprojection", "Cos(theta) SM projection")
BSMhisto.Write()
SMhisto.Write()

BSMhisto1 = h_S0.ProjectionX()
SMhisto1 = electronHisto.ProjectionX()
BSMhisto1.SetNameTitle("xBSMprojection", "x BSM projection")
SMhisto1.SetNameTitle("xSMprojection", "x SM projection")
BSMhisto1.Write()
SMhisto1.Write()

savingFile.Close()
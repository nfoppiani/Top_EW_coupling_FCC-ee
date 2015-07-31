from ROOT import TFile, TCanvas, TH2F
import numpy
import glob

myfile_mc = TFile("../plot/2dWhizardPositronHisto.root","READ")
myfile_an = TFile("../analytic/SMCross.root","READ")

h_mc=TH2F("ciao","ciao",40,0.,1.4,30,-1.,1.)
h_an=TH2F("ciao","ciao",40,0.,1.4,30,-1.,1.)

h_mc = myfile_mc.Get("electronReducedEnergyAndAngleHisto")
h_an = myfile_an.Get("smcross")

h_mc.Divide(h_an)

c_ratio = TCanvas("Ratio MC/An","Ratio MC/An",800,800)
c_ratio.cd()
h_mc.Draw("surf")

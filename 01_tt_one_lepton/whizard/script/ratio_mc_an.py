from ROOT import TFile, TCanvas, TH2F
import numpy
import glob

myfile_mc = TFile("../plot/2dWhizardPositronHisto.root","READ")
myfile_an = TFile("../analytic/SMCross.root","READ")

h_mc=TH2F(" "," ",40,0.,1.4,30,-1.,1.)
h_an=TH2F(" "," ",40,0.,1.4,30,-1.,1.)

h_mc = myfile_mc.Get("electronReducedEnergyAndAngleHisto")
h_an = myfile_an.Get("smcross")

c_mc = TCanvas("Montecarlo electron distribution","Montecarlo electron distribution",800,800)
c_mc.cd()
h_mc.Draw("surf")

c_an = TCanvas("Analytic electron distribution","Analytic electron distribution",800,800)
c_an.cd()
h_an.Draw("surf")

h_mc.Divide(h_an)

c_ratio = TCanvas("Ratio MC An","Ratio MC An",800,800)
c_ratio.cd()
h_mc.Draw("surf")


#saving the histograms

print "I am saving the histos"

el_distribution_mc_an = TFile("./../plot/electron_distribution_mc_an_histo.root","CREATE")
h_mc.Write()
h_an.Write()
#h_mc.Write()

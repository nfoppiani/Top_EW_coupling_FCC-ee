from ROOT import TFile, TCanvas, TH2F, TH1F
import numpy

a_min=-0.75

#getting the analytic histograms

myfile_an = TFile("../analytic/Histo_S0_f1_SM.root","READ")
saving_file=TFile("../plot/comparing_histo_energy.root","CREATE")

h_S0 = myfile_an.Get("smcross")
h_f1 = myfile_an.Get("FBzed")

#h_S0.Scale(1/h_S0.Integral())
#h_f1.Scale(1/h_f1.Integral())

#getting the montecarlo histogram

myfile_mc = TFile("../plot/electrons_histo.root","READ")

h_mc = myfile_mc.Get("mc_electrons")

######plot of the marginal energy projectons

	#montecarlo
h_EN_mc = h_mc.ProjectionX("montecarlo_energy")

#c_mc=TCanvas("Montecarlo electron energy","Montecarlo electron energy",800,800)
#c_mc.cd()
#h_EN_mc.Draw()
h_EN_mc.Scale(1/h_EN_mc.Integral())

saving_file.cd()
h_EN_mc.Write()

	#without BSM correction
h_EN_S0= h_S0.ProjectionX("S0_energy")

h_EN_S0.Scale(1/h_EN_S0.Integral())

#c_S0=TCanvas("Analytical SM electron energy","Analytical SM electron energy",800,800)
#c_S0.cd()
#h_EN_S0.Draw()

saving_file.cd()
h_EN_S0.Write()

	#with BSM correction

#h_EN_bsm2= TH2F("Analytical BSM electron energy with a=0.22","Analytical BSM electron energy with a=0.22",200,0.112426,1.,200,-1.,1.)

#h_EN_bsm2.Add(h_f1,a_min)
#h_EN_bsm2.Add(h_S0)

h_EN_bsm2 = h_S0

h_EN_bsm2.Add(h_f1,a_min)

h_EN_bsm1= h_EN_bsm2.ProjectionX("BSM_energy")

h_EN_bsm1.Scale(1/h_EN_bsm1.Integral())

saving_file.cd()
h_EN_bsm1.Write()

#c_bsm=TCanvas("Analytical BSM electron energy with a=0.22","Analytical BSM electron energy with a=0.22",800,800)
#c_bsm.cd()
#h_EN_bsm1.Draw()

from ROOT import TFile, TCanvas, TH2F, TH1F
import numpy

a=numpy.array([0.005,-0.08])

#getting the analytic histograms

myfile_an = TFile("../analytic/SMCrossWhizard364.root","READ")
saving_file=TFile("../plot/comparing_histo_angle.root","CREATE")

h_S0 = myfile_an.Get("smcross")
h_f1 = myfile_an.Get("FBzed")
h_f2 = myfile_an.Get("FBzed")

#h_S0.Scale(1/h_S0.Integral())
#h_f1.Scale(1/h_f1.Integral())

#getting the montecarlo histogram

myfile_mc = TFile("../plot/2dWhizardLeptons200Histo.root","READ")
h_mc = myfile_mc.Get("electronReducedEnergyAndAngleHisto")

#####plot of the marginal costheta projectons

#montecarlo
h_angle_mc = h_mc.ProjectionY("montecarlo_angle")

#c_mc_angle=TCanvas("Montecarlo electron angle","Montecarlo electron angle",800,800)
#c_mc_angle.cd()
#h_angle_mc.Draw()
h_angle_mc.Scale(1/h_angle_mc.Integral())

saving_file.cd()
h_angle_mc.Write()

#without BSM correction
h_angle_S0= h_S0.ProjectionY("S0_angle")

h_angle_S0.Scale(1/h_angle_S0.Integral())
#c_S0_angle=TCanvas("Analytical SM electron angle","Analytical SM electron angle",800,800)
#c_S0_angle.cd()
#h_angle_S0.Draw()

saving_file.cd()
h_angle_S0.Write()

#with BSM correction
h_angle_bsm2 = h_S0

h_angle_bsm2.Add(h_f1,a[0])
h_angle_bsm2.Add(h_f1,a[1])

h_angle_bsm1= h_angle_bsm2.ProjectionY("BSM_angle")

h_angle_bsm1.Scale(1/h_angle_bsm1.Integral())

saving_file.cd()
h_angle_bsm1.Write()

#c_bsm_angle=TCanvas("Analytical BSM electron energy with a=0.22","Analytical BSM electron energy with a=0.22",800,800)
#c_bsm_angle.cd()
#h_angle_bsm1.Draw()


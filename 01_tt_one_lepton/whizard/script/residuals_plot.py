from ROOT import TFile, TCanvas, TH2F, TH1F

myfile = TFile("../plot/comparing_histo_angle.root","UPDATE")

hMc=myfile.Get("montecarlo_angle")
hS0=myfile.Get("S0_angle")
hBsm=myfile.Get("BSM_angle")

hMc.Add(hBsm,-1)
myfile.cd()
hMc.Write("BSM_residuals")

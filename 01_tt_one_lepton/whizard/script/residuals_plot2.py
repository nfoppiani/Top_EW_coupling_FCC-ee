from ROOT import TFile, TCanvas, TH2F, TH1F

myfile = TFile("../plot/comparing_histo_angle.root","OPEN")

hMc=myfile.Get("montecarlo_angle")

hS0=myfile.Get("S0_angle")
hS0.SetNameTitle("MC and S0 electrons angular distribution","MC and S0 electrons angular distribution")

hBSM=myfile.Get("BSM_angle")
hBSM.SetNameTitle("MC and BSM fit electrons angular distribution","MC and BSM fit electrons angular distribution")

hS0residuals=myfile.Get("S0_residuals")
hS0residuals.SetNameTitle("residuals MC S0","residuals MC S0")

hBSMresiduals=myfile.Get("BSM_residuals")
hBSMresiduals.SetNameTitle("residuals MC BSM fit","residuals MC BSM fit")

c1=TCanvas("MC S0 angular distribution","MC S0 angular distribution",800,800)
c1.Divide(1,2)

c1.cd(1)
hS0.Draw()
hMc.Draw("same")


c1.cd(2)
hS0residuals.Draw()

c2=TCanvas("MC BSM angular distribution","MC BSM angular distribution",800,800)
c2.Divide(1,2)

c2.cd(1)
hBSM.Draw()
hMc.Draw("same")


c2.cd(2)
hBSMresiduals.Draw()

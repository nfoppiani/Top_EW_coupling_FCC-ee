from ROOT import TFile, TLorentzVector
import numpy
from particleClass import *
from findElectrons import *

file = TFile('./../ntuple/electrons_ntuple/yyxyev_o_*.root',"READ")
tree = file.Get("MyLCTuple")

savingFile=TFile('./../plot/electrons_acceptance',"CREATE")

hCosTheta=TH1F("cosTheta REC / cosTheta mc","cosTheta REC / cosTheta mc",40,0.,2.)

hEnergy=TH1F("Energy REC / Energy mc","cosTheta REC / cosTheta mc",40,0.,2.)

hElRec=TH2F("Energy-angle REC electron distribution","Energy-angle REC electron distribution",20,10.,120.,20,-1.,1.)

hElMc=TH2F("Energy-angle MC electron distribution","Energy-angle MC electron distribution",20,10.,120.,20,-1.,1.)

hCosTheta.Fill(
hEnergy.Fill(
hElRec.Fill(
hElMc.Fill(

savingFile.cd()
hCosTheta.Write()
hEnergy.Write()
hElRec.Write()
hElMc.Write()

#projection of the 2d histograms

hElRec.Divide(hElMc)

hElRecMc_energy=hElRec.ProjectionX("Energy Electrons REC / Electrons MC")

hElRecMc_cosTheta=hElRec.ProjectionY("cosTheta Electrons REC / Electrons MC")

savingFile.cd()
hElRecMc_energy.Write()
hElRecMc_cosTheta.Write()

# 1. counts the number of reconstructed muons per event and fills the relative histogram
# 2. plots the angle (in degrees) between the rc muons and the mc muons for the events with three or more muons

from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain, T
from numpy import degrees
from particleClass import *

tree = TChain("MyLCTuple")
tree.Add('./../whizard_negMuTau_yyxylv/000/yyxylv_o_*.root')
tree.Add('./../whizard_negMuTau_yyxylv/001/yyxylv_o_*.root')

hMuonsPerEvent = TH1F("muonsPerEvent","Number of RC muons per event",10,0.,9.)
hMoreThan3Angle = TH1F("moreThan3Angle","Angle between RC muons and MC W-decay one for events with three RC muons or more",360,0.,180)
hMoreThan3NearestAngle = TH1F("moreThan3NearestAngle","Angle between MC W-decay muon and nearest RC one for events with three RC muons or more",360,0.,180)
hMoreThan3NotNearestAngle = TH1F("moreThan3NearestAngle","Angle between MC W-decay muon and not-nearest RC ones for events with three RC muons or more",360,0.,180)




for event in tree:
    if tree.mcpdg[10]==13:
        count = 0
        mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])
        
        rcMuons = []
        for i in range(len(tree.rctyp)):
            if tree.rctyp[i] == 13:
                p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
                rcMuons.append(p)
                count += 1
        
        hMuonsPerEvent.Fill(count)

        if count >= 3:
            minAngle = numpy.pi
            minAngleNumber = -1
            for i in len(rcMuons):
                angle = rcMuons[i].angle(mcMuon)
                if angle < minAngle:
                    minAngle = angle
                    minAngleNumber = i
                hMoreThan3Angle.Fill(degrees(angle))


savingFile=TFile('./muonsPerEvent.root',"RECREATE")
savingFile.cd()
hMuonsPerEvent.Write()
hMoreThan3Angle.Write()
savingFile.Close()
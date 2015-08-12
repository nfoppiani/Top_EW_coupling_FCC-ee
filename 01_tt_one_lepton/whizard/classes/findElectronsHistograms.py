from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain
import numpy
from particleClass import *
from findElectrons import *

energyCut=10.

def findElectronConeChargedParticle(rcList):
    cosMin = 1
    number = -1
    for el in rcList:
        if el.type == 11 and el.p.E() > energyCut:
            cosMax = -1
            for part in rcList:
                if part.type != 11 and part.type != -11 and part.type != 22:
                    ang = el.angle(part)
                    cos = numpy.cos(ang)
                    if cos > cosMax:
                        if part.num != el.num:
                            cosMax = cos
            if cosMax < cosMin:
                cosMin = cosMax
                number = el.num
    return number
    


tree = TChain("MyLCTuple")
tree.Add('./../ntuple/electrons_ntuple/yyxyev_o_*.root')

savingFile=TFile('./../plot/electrons_acceptance.root',"RECREATE")

hCosTheta=TH1F("cosTheta REC / cosTheta mc","cosTheta REC / cosTheta mc",40,0.,2.)

hEnergy=TH1F("Energy REC / Energy mc","Energy REC / Energy mc",40,0.,2.)

hElRec=TH2F("Energy-angle REC electron distribution","Energy-angle REC electron distribution",20,10.,120.,20,-1.,1.)

hElMc=TH2F("Energy-angle MC electron distribution","Energy-angle MC electron distribution",20,10.,120.,20,-1.,1.)

hRecCosThetaTotal=TH1F("cosTheta REC distribution","cosTheta REC distribution",40,-1.,1.)

hMcCosThetaTotal=TH1F("cosTheta MC distribution","cosTheta MC distribution",40,-1.,1.)



#hDeltaEoverE=TH1F("DeltaE over E as a function of E","DeltaE over E as a function of E"

found=0

for event in tree:
    found=0
    rcParticles = []
    for i in range(len(tree.rctyp)):
        p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
        rcParticles.append(p)
    
    #for i in range(len(rcParticles)):
    #    rcParticles[i].sumPhotons(rcParticles)

    rcJets = []
    for i in range(len(tree.jene)):
        p = Jet(i,tree.jmas[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
        rcJets.append(p)
        
	num=findElectronPtMaxClosestJet(rcParticles,rcJets)
	found=rcParticles[num]
	mcElectron = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])
	hCosTheta.Fill(found.cosTheta()/mcElectron.cosTheta())
	hEnergy.Fill(found.p.E()/mcElectron.p.E())
	hElRec.Fill(found.p.E(),found.cosTheta())
	hElMc.Fill(mcElectron.p.E(),mcElectron.cosTheta())
	hRecCosThetaTotal.Fill(found.cosTheta())
	hMcCosThetaTotal.Fill(mcElectron.cosTheta())
	
savingFile.cd()
hCosTheta.Write()
hEnergy.Write()
hElRec.Write()
hElMc.Write()

hRecCosThetaTotal.Divide(hMcCosThetaTotal)
savingFile.cd()
hRecCosThetaTotal.Write("Total cosTheta REC/total cosTheta MC")

##projection of the 2d histograms

#hElRec.Divide(hElMc)

##hElRec.Write("ratio_rc_mc")

#hElRecMc_energy=hElRec.ProjectionX("Energy Electrons REC / Electrons MC")

#hElRecMc_cosTheta=hElRec.ProjectionY("cosTheta Electrons REC / Electrons MC")

#savingFile.cd()
#hElRecMc_energy.Write("Energy Electrons REC / Electrons MC")
#hElRecMc_cosTheta.Write("cosTheta Electrons REC / Electrons MC")

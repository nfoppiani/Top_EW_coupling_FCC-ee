from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain, THStack, TGraph
import numpy
from particleClass import *
#from findElectrons import *

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')


#this script calculates the efficiency and purity with cut at form of L near the origin for the two dim algoritm "pt to the closest jet" and "angle to closest charged.

#definition of area

angleMax=0.5
pTMax=45.

#angleMin=numpy.array([0.01,0.05,0.08,0.10,0.12,0.15,0.18,0.20,0.25,0.3])
angleMin=0.08

pTMin=numpy.array([0.5,6.,7.,8.,9.,10.,11.,12.,13.,140.])


generatedMuons=0
matched=numpy.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])
nonMatched=numpy.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])

efficiency=numpy.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])
purity=numpy.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])


for event in tree:
    if tree.mcpdg[10]==13:
        mcMuon = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])
        rcParticles = []
        for i in range(len(tree.rctyp)):
            p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
            rcParticles.append(p)

        rcJets = []
        for i in range(len(tree.jene)):
                        p = Jet(i,tree.jmas[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
                        rcJets.append(p)

        MatchNum = mcMuon.matchMuon(rcParticles)

        if MatchNum != -1:
            Pt=rcParticles[MatchNum].ptToClosestJet(rcJets)
            Angle=rcParticles[MatchNum].angleToClosestCharge(rcParticles)

            for i in range(len(pTMin)):
                if (Angle>angleMax) or (Pt>=pTMin[i] and Pt<=pTMax and Angle>angleMin) or (Pt>=pTMax):
                    matched[i] += 1

        for part in rcParticles:
            if part.type ==13 and part.num!=MatchNum:
                Pt=part.ptToClosestJet(rcJets)                
                Angle=part.angleToClosestCharge(rcParticles)

                for i in range(len(pTMin)):
                    if (Angle>angleMax) or (Pt>=pTMin[i] and Pt<=pTMax and Angle>angleMin) or (Pt>=pTMax):
                        nonMatched[i] += 1
                        

        generatedMuons += 1

for i in range(len(pTMin)):
    print "ptmin",i, pTMin[i]
    efficiency[i] = matched[i]/generatedMuons
    print "efficiency",i, efficiency[i]
    if (matched[i]+nonMatched[i])>0:
        purity[i]=1-(nonMatched[i]/(matched[i]+nonMatched[i]))
        print "purity",i, purity[i]

Eff=TGraph(len(pTMin),pTMin,efficiency)
Pur=TGraph(len(pTMin),pTMin,purity)

Eff.Draw()
Pur.Draw("same")

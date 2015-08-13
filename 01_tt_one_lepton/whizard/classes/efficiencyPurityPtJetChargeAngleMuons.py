from ROOT import TFile, TLorentzVector, TH1F, TH2F, TChain, THStack, TGraph
import numpy
from particleClass import *
#from findElectrons import *

tree = TChain("MyLCTuple")
tree.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')


#this script calculates the efficiency and purity with cut at form of L near the origin for the two dim algoritm "pt to the closest jet" and "angle to closest charged.

#definition of area

pTMax=4.

angleMax=numpy.array([0.2,0.25,0.03,0.35,0.40,0.45,0.50,0.55,0.60,0.65])


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
                        p = Jet(i,tree.jmas[i],tree.jcha[i],tree.jmox[i],tree.jmoy[i],tree.jmoz[i],tree.jene[i])
                        rcJets.append(p)

        MatchNum = mcMuon.matchMuon(rcParticles)

        if MatchNum != -1:
            Pt=rcParticles[MatchNum].ptToClosestJet(rcJets)
            Angle=rcParticles[MatchNum].angleToClosestCharge(rcParticles)

            for i in range(len(angleMax)):
                if (Angle>=angleMax[i]) or (Pt>=pTMax):
                    matched[i] += 1

        for part in rcParticles:
            if part.typ ==13 and part.num!=MatchNum:
                Pt=part.ptToClosestJet(rcJets)                
                Angle=part.angleToClosestCharge(rcParticles)

                for i in range(len(angleMax)):
                    if (Angle>=angleMax[i]) or (Pt>=pTMax):
                        nonMatched[i] += 1
                        

        generatedMuons += 1

for i in range(len(angleMax)):
    print "angleMax",i, angleMax[i]
    efficiency[i] = matched[i]/generatedMuons
    print "efficiency",i, efficiency[i]
    if (matched[i]+nonMatched[i])>0:
        purity[i]=1-(nonMatched[i]/(matched[i]+nonMatched[i]))
        print "purity",i, purity[i]

Eff=TGraph(len(angleMax),angleMax,efficiency)
Pur=TGraph(len(angleMax),angleMax,purity)

Eff.Draw()
Pur.Draw("same")

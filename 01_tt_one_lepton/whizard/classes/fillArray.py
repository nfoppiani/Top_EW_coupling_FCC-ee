from ROOT import TFile, TLorentzVector, TH2D
import numpy
import glob
from particleClass import *
from findElectrons import *

fileList = glob.glob('./../whizard_electron_yyxyev/yyxyev*1.root')

rightCos = 0.95
rightDist = 10

wrongEnergy = 170
wrongCos = -0.8

hFindElectronPtMax = TH2D("findElectronPtMax", "Wrong founds", 28, 0., 180., 20, -1., 1.)
hFindElectronPtMaxClosestJet = TH2D("findElectronPtMaxClosestJet", "Wrong founds", 28, 0., 180., 20, -1., 1.)
hFindElectronConeChargedParticle = TH2D("findElectronConeChargedParticle", "Wrong founds", 28, 0., 180., 20, -1., 1.)
hFindElectronConeChargedNotElectronParticle = TH2D("findElectronConeChargedNotElectronParticle", "Wrong founds", 28, 0., 180., 20, -1., 1.)
hFindElectronConeChargedNotElectronPositronParticle = TH2D("findElectronConeChargedNotElectronPositronParticle", "Wrong founds", 28, 0., 180., 20, -1., 1.)

k = 0

for fileName in fileList:
    file = TFile(fileName,"READ")
    tree = file.Get("MyLCTuple")

    for event in tree:
        
        rcParticles = []
        for i in range(len(tree.rctyp)):
            p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
            rcParticles.append(p)
        
        for i in range(len(rcParticles)):
            rcParticles[i].sumPhotons(rcParticles)

        rcJets = []
        for i in range(len(tree.jene)):
            p = Jet(i,tree.jmas[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
            rcJets.append(p)


        mcElectron = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])





        electronNumber = findElectronPtMax(rcParticles, rcJets)
        if electronNumber != -1:
            ang = mcElectron.angle(rcParticles[electronNumber])
            cos = numpy.cos(ang)
            dist = Distance(rcParticles[electronNumber],mcElectron)
            if cos < rightCos or dist > rightDist:
                hFindElectronPtMax.Fill(rcParticles[electronNumber].p.E(), rcParticles[electronNumber].cosTheta())
        else:
            hFindElectronPtMax.Fill(wrongEnergy, wrongCos)
        
        electronNumber = findElectronPtMaxClosestJet(rcParticles, rcJets)
        if electronNumber != -1:
            ang = mcElectron.angle(rcParticles[electronNumber])
            cos = numpy.cos(ang)
            dist = Distance(rcParticles[electronNumber],mcElectron)
            if cos < rightCos or dist > rightDist:
                hFindElectronPtMaxClosestJet.Fill(rcParticles[electronNumber].p.E(), rcParticles[electronNumber].cosTheta())
        else:
            hFindElectronPtMaxClosestJet.Fill(wrongEnergy, wrongCos)
        
        electronNumber = findElectronConeChargedParticle(rcParticles)
        if electronNumber != -1:
            ang = mcElectron.angle(rcParticles[electronNumber])
            cos = numpy.cos(ang)
            dist = Distance(rcParticles[electronNumber],mcElectron)
            if cos < rightCos or dist > rightDist:
                hFindElectronConeChargedParticle.Fill(rcParticles[electronNumber].p.E(), rcParticles[electronNumber].cosTheta())
        else:
            hFindElectronConeChargedParticle.Fill(wrongEnergy, wrongCos)

        electronNumber = findElectronConeChargedNotElectronParticle(rcParticles)
        if electronNumber != -1:
            ang = mcElectron.angle(rcParticles[electronNumber])
            cos = numpy.cos(ang)
            dist = Distance(rcParticles[electronNumber],mcElectron)
            if cos < rightCos or dist > rightDist:
                hFindElectronConeChargedNotElectronParticle.Fill(rcParticles[electronNumber].p.E(), rcParticles[electronNumber].cosTheta())
        else:
            hFindElectronConeChargedNotElectronParticle.Fill(wrongEnergy, wrongCos)

        electronNumber = findElectronConeChargedNotElectronPositronParticle(rcParticles)
        if electronNumber != -1:
            ang = mcElectron.angle(rcParticles[electronNumber])
            cos = numpy.cos(ang)
            dist = Distance(rcParticles[electronNumber],mcElectron)
            if cos < rightCos or dist > rightDist:
                hFindElectronConeChargedNotElectronPositronParticle.Fill(rcParticles[electronNumber].p.E(), rcParticles[electronNumber].cosTheta())
        else:
            hFindElectronConeChargedNotElectronPositronParticle.Fill(wrongEnergy, wrongCos)

        k = k+1

print k


savingFile = TFile("./compareFindingMethods.root", "CREATE")
hFindElectronPtMax.Write()
hFindElectronPtMaxClosestJet.Write()
hFindElectronConeChargedParticle.Write()
hFindElectronConeChargedNotElectronParticle.Write()
hFindElectronConeChargedNotElectronPositronParticle.Write()
savingFile.Close()
    
'''
        distance = Distance(rcParticles[electronNumber],mcElectron)
        distance1 = Distance(rcParticles[electronNumber1],mcElectron)
        ang = mcElectron.angle(rcParticles[electronNumber])
        ang1 = mcElectron.angle(rcParticles[electronNumber1])
        cos = numpy.cos(ang)
        cos1 = numpy.cos(ang1)

        if cos < 0.95:
            err += 1
        if cos1 < 0.95:
            err1 += 1

        if rcParticles[electronNumber].p.E() > rcParticles[electronNumber1].p.E():
            cosTrue = cos
        else:
            cosTrue = cos1

        if cosTrue < 0.95:
            botherr += 1

        print 'EVENT\t', k
        print 'elNum\t', electronNumber, '\t\t', electronNumber1
        print 'mcDist\t', distance, '\t', distance1
        print 'mcCos\t', cos, '\t', cos1
        print 'rcEne\t', rcParticles[electronNumber].p.E(), '\t', rcParticles[electronNumber1].p.E()
        print 'mcCos\t', mcElectron.cosTheta()
        print
        k = k+1
    
print err1
print botherr
'''
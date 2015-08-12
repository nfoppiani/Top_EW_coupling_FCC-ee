from ROOT import TFile, TLorentzVector, TH1F
import numpy
import glob
from particleClass import *
from findElectrons import *

#file = TFile('./../ntuple/electrons_ntuple/yyxyev_o_*.root',"READ")
fileList = glob.glob('./yyxyev_o_1.root')

#energyDeltaHisto = TH1F("energyDelta", "Difference between RC-isolated and MC electron", 80, -30., 30.)

#err = 0

for fileName in fileList:
    file = TFile(fileName,"READ")
    tree = file.Get("MyLCTuple")
    k = 0

    for event in tree:
        print 'EVENT', k
        rcParticles = []
        for i in range(len(tree.rctyp)):
            p = Particle(i, tree.rctyp[i],tree.rccha[i],tree.rcmox[i],tree.rcmoy[i],tree.rcmoz[i],tree.rcene[i])
            rcParticles.append(p)
        
        for i in range(len(rcParticles)):
            rcParticles[i].sumPhotonsRectangle(rcParticles)
        k = k+1


'''
        mcElectron = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])

        electronNumber = findElectronConeChargedNotElectronParticle(rcParticles)
        distance = Distance(rcParticles[electronNumber],mcElectron)
        ang = mcElectron.angle(rcParticles[electronNumber])
        cos = numpy.cos(ang)

        if cos < 0.95:
            err += 1
        else:
            energyDeltaHisto.Fill(rcParticles[electronNumber].p.E()-mcElectron.p.E())
        k = k+1

print err

savingFile = TFile("./photonsCalibration.root", "CREATE")
energyDeltaHisto.Write()
savingFile.Close()
'''
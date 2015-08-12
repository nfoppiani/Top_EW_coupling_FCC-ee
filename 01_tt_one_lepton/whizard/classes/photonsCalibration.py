from ROOT import TFile, TLorentzVector, TH1F
import numpy
import glob
from particleClass import *
from findElectrons import *

electronMatchMinEnergy = 10


#file = TFile('./../ntuple/electrons_ntuple/yyxyev_o_*.root',"READ")
fileList = glob.glob('./yyxyev_o_1.root')

#energyDeltaHisto = TH1F("energyDelta", "Difference between RC-isolated and MC electron", 80, -30., 30.)

err = 0
sum = 0
errDecay = 0
sumDecay = 0

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

        #for i in range(len(rcParticles)):
         #   rcParticles[i].sumPhotonsCone(rcParticles)
        rcElectron = []
        for i in range(len(tree.mcpdg)):
            if tree.mcpdg[i] == 11 and tree.mcene[i] > electronMatchMinEnergy:
                p = Particle(i, tree.mcpdg[i],tree.mccha[i],tree.mcmox[i],tree.mcmoy[i],tree.mcmoz[i],tree.mcene[i])
                rcElectron = p.matchElectron(rcParticles)
                if rcElectron[0] == -1:
                    err += 1
                else:
                    sum += rcElectron[1]
        
        print
        mcDecayElectron = Particle(10,tree.mcpdg[10],tree.mccha[10],tree.mcmox[10],tree.mcmoy[10],tree.mcmoz[10],tree.mcene[10])
        rcDecayElectron=[]
        rcDecayElectron = mcDecayElectron.matchElectron(rcParticles)
        if rcDecayElectron[0] == -1:
            errDecay += 1
        else:
            sumDecay += rcDecayElectron[1]
        k = k+1

print
print 'not found', err
print 'tot distance', sum
print 'not found decays', errDecay
print 'tot decay distance', sumDecay

'''
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
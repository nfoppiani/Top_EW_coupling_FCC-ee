from ROOT import TFile, TLorentzVector
import numpy
from particleClass import *
from findElectrons import *

file = TFile('./../ntuple/electrons_ntuple/yyxyev_o_*.root',"READ")
tree = file.Get("MyLCTuple")

k = 0

err = 0
err1 = 0
botherr = 0

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
    electronNumber1 = findElectronConeChargedParticle(rcParticles)
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
'''
    print 'EVENT\t', k
    print 'elNum\t', electronNumber, '\t\t', electronNumber1
    print 'mcDist\t', distance, '\t', distance1
    print 'mcCos\t', cos, '\t', cos1
    print 'rcEne\t', rcParticles[electronNumber].p.E(), '\t', rcParticles[electronNumber1].p.E()
    print 'mcCos\t', mcElectron.cosTheta()
    print
'''

    k = k+1

print err
print err1
print botherr
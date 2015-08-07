# This file produces the 2-dimentional histos of the leptons, divided per family and charge, in function of the reduced energy and of the cosine of the polar angle

from ROOT import TFile, TH2D
import glob
from numpy import sqrt

#################################
### REDUCED ENERGY DEFINITION ###
#################################

top = 174.          # top mass
w = 80.419          # w boson mass
s = 365.**2         # center of mass squared energy

beta = sqrt(1-4*top**2/s)               # beta=v/c of the top
r = w**2/top**2
red = 2/top*sqrt((1-beta)/(1+beta))     # reduction factor: REDUCED ENERGY = xf = energy*red
xfMin = r*(1-beta)/(1+beta)             # minimum xf value (maximum is 1)

print 'beta = ', beta
print 'red = ', red
print 'xfMax = 1'
print 'xfMin = ', xfMin


##############################
### HISTOGRAMS DECLARATION ###
##############################

hElectron = TH2D("electronReducedEnergyAndAngleHisto", "W-decay electrons reduced energy and cosine of polar angle", 40, 0., 1.4, 30, -1., 1.)
hPositron = TH2D("positronReducedEnergyAndAngleHisto", "W-decay positrons reduced energy and cosine of polar angle", 40, 0., 1.4, 30, -1., 1.)
hLightLeptons = TH2D("lightLeptonsReducedEnergyAndAngleHisto", "W-decay electrons and positrons reduced energy and cosine of polar angle (multiplied per -1 for positrons)", 40, 0., 1.4, 30, -1., 1.)
hPositiveMuon = TH2D("positiveMuonReducedEnergyAndAngleHisto", "W-decay positive muons reduced energy and cosine of polar angle", 40, 0., 1.4, 30, -1., 1.)
hNegativeMuon = TH2D("negativeMuonReducedEnergyAndAngleHisto", "W-decay negative muons reduced energy and cosine of polar angle", 40, 0., 1.4, 30, -1., 1.)
hMuon = TH2D("muonsReducedEnergyAndAngleHisto", "W-decay muons reduced energy and cosine of polar angle (multiplied per -1 for positive muons)", 40, 0., 1.4, 30, -1., 1.)
hPositiveTau = TH2D("positiveTauReducedEnergyAndAngleHisto", "W-decay positive taus reduced energy and cosine of polar angle", 40, 0., 1.4, 30, -1., 1.)
hNegativeTau = TH2D("negativeTauReducedEnergyAndAngleHisto", "W-decay negative taus reduced energy and cosine of polar angle", 40, 0., 1.4, 30, -1., 1.)
hTau = TH2D("tauReducedEnergyAndAngleHisto", "W-decay taus reduced energy and cosine of polar angle (multiplied per -1 for positive muons)", 40, 0., 1.4, 30, -1., 1.)
hPositiveLeptons = TH2D("positiveLeptonsReducedEnergyAndAngleHisto", "W-decay positive leptons reduced energy and cosine of polar angle", 40, 0., 1.4, 30, -1., 1.)
hNegativeLeptons = TH2D("negativeLeptonsReducedEnergyAndAngleHisto", "W-decay negative leptons reduced energy and cosine of polar angle", 40, 0., 1.4, 30, -1., 1.)
hLeptons = TH2D("leptonsReducedEnergyAndAngleHisto", "W-decay leptons reduced energy and cosine of polar angle (multiplied per -1 for positive muons)", 40, 0., 1.4, 30, -1., 1.)

#################
### POSITRONS ###
#################

# records the yy*.root files list of the whizard_positron_yyveyx directory
fileList = glob.glob('./whizard_positron_yyveyx/yy*.root')

for fileName in fileList:
    # reads the yy*.root file
    file = TFile(fileName,"READ")
    tree = file.Get("MyLCTuple")
    
    # loops over the 99 events of the tree
    for event in tree:
        control = 1
        if tree.mcpdg[9] == -11:                                # the W-decay positron has progressive number 9
            energy = tree.mcene[9]
            px = tree.mcmox[9]
            py = tree.mcmoy[9]
            pz = tree.mcmoz[9]
            cosTheta = pz/sqrt(px**2+py**2+pz**2)
            hPositron.Fill(energy*red, -cosTheta)                # cosTheta*(-1) to have the same electrons distribution!
            if tree.mcpdg[8] == 12:                             # the relative neutrino has progressive number 8
                control = 0
        if control == 1:                                        # checks that W-decay positrons and neutrinos have progressive numbers 9 and 8
            print 'error positron'
    file.Close()

print 'End of positrons'

#################
### ELECTRONS ###
#################

# records the yy*.root files list of the whizard_electron_yyxyev directory
fileList = glob.glob('./whizard_electron_yyxyev/yy*.root')

for fileName in fileList:
    # reads the yy*.root file
    file = TFile(fileName,"READ")
    tree = file.Get("MyLCTuple")
    
    # loops over the 99 events of the tree
    for event in tree:
        control = 1
        if tree.mcpdg[10] == 11:                        # W-decay electrons have progressive number 10
            energy = tree.mcene[10]
            px = tree.mcmox[10]
            py = tree.mcmoy[10]
            pz = tree.mcmoz[10]
            cosTheta = pz/sqrt(px**2+py**2+pz**2)
            hElectron.Fill(energy*red, cosTheta)
            if tree.mcpdg[11] == -12:                   # relative antineutrinos have progressive number 11
                control = 0
        if control == 1:                                # checks that W-decay electrons and neutrinos have progressive numbers 10 and 11
            print 'error electron'
    file.Close()

print 'End of electrons'

##############################
### NEGATIVE HEAVY LEPTONS ###
##############################

# records the yy*.root files list of the whizard_negMuTau_yyxylv/000/ directory
fileList = glob.glob('./whizard_negMuTau_yyxylv/000/yy*.root')

for fileName in fileList:
    # reads the yy*.root file
    file = TFile(fileName,"READ")
    tree = file.Get("MyLCTuple")
    
    # loops over the 99 events of the tree
    for event in tree:
        control = 1
        if tree.mcpdg[10] == 13:                                # the W-decay muon- has progressive number 10
            energy = tree.mcene[10]
            px = tree.mcmox[10]
            py = tree.mcmoy[10]
            pz = tree.mcmoz[10]
            cosTheta = pz/sqrt(px**2+py**2+pz**2)
            hNegativeMuon.Fill(energy*red, cosTheta)
            if tree.mcpdg[11] == -14:                             # the relative antineutrino has progressive number -14
                control = 0
        if tree.mcpdg[10] == 15:                                # the W-decay tau- has progressive number 10
            energy = tree.mcene[10]
            px = tree.mcmox[10]
            py = tree.mcmoy[10]
            pz = tree.mcmoz[10]
            cosTheta = pz/sqrt(px**2+py**2+pz**2)
            hNegativeTau.Fill(energy*red, cosTheta)
            if tree.mcpdg[11] == -16:                             # the relative antineutrino has progressive number -16
                control = 0
        if control == 1:                                        # checks that W-decay taus-/muons- and neutrinos have progressive numbers 10 and 11
            print 'error mu-/tau-'
    file.Close()

print 'End of negative heavy leptons - 000'

# records the yy*.root files list of the whizard_negMuTau_yyxylv/000/ directory
fileList = glob.glob('./whizard_negMuTau_yyxylv/000/yy*.root')

for fileName in fileList:
    # reads the yy*.root file
    file = TFile(fileName,"READ")
    tree = file.Get("MyLCTuple")
    
    # loops over the 99 events of the tree
    for event in tree:
        control = 1
        if tree.mcpdg[10] == 13:                                # the W-decay muon- has progressive number 10
            energy = tree.mcene[10]
            px = tree.mcmox[10]
            py = tree.mcmoy[10]
            pz = tree.mcmoz[10]
            cosTheta = pz/sqrt(px**2+py**2+pz**2)
            hNegativeMuon.Fill(energy*red, cosTheta)
            if tree.mcpdg[11] == -14:                             # the relative antineutrino has progressive number 11
                control = 0
        if tree.mcpdg[10] == 15:                                # the W-decay tau- has progressive number 10
            energy = tree.mcene[10]
            px = tree.mcmox[10]
            py = tree.mcmoy[10]
            pz = tree.mcmoz[10]
            cosTheta = pz/sqrt(px**2+py**2+pz**2)
            hNegativeTau.Fill(energy*red, cosTheta)
            if tree.mcpdg[11] == -16:                             # the relative antineutrino has progressive number 16
                control = 0
        if control == 1:                                        # checks that W-decay taus-/muons- and antineutrinos have progressive numbers 10 and 11
            print 'error mu-/tau-'
    file.Close()

print 'End of positive heavy leptons - 001'

##############################
### POSITIVE HEAVY LEPTONS ###
##############################

# records the yy*.root files list of the whizard_posMuTau_yyvlyx directory
fileList = glob.glob('./whizard_posMuTau_yyvlyx/000/yy*.root')

for fileName in fileList:
    # reads the yy*.root file
    file = TFile(fileName,"READ")
    tree = file.Get("MyLCTuple")
    
    # loops over the 99 events of the tree
    for event in tree:
        control = 1
        if tree.mcpdg[9] == -13:                        # W-decay muon+ have progressive number 9
            energy = tree.mcene[9]
            px = tree.mcmox[9]
            py = tree.mcmoy[9]
            pz = tree.mcmoz[9]
            cosTheta = pz/sqrt(px**2+py**2+pz**2)
            hPositiveMuon.Fill(energy*red, -cosTheta)
            if tree.mcpdg[8] == 14:                   # relative neutrinos have progressive number 8
                control = 0
        if tree.mcpdg[9] == -15:                        # W-decay tau+ have progressive number 9
            energy = tree.mcene[9]
            px = tree.mcmox[9]
            py = tree.mcmoy[9]
            pz = tree.mcmoz[9]
            cosTheta = pz/sqrt(px**2+py**2+pz**2)
            hPositiveTau.Fill(energy*red, -cosTheta)
            if tree.mcpdg[8] == 16:                   # relative neutrinos have progressive number 8
                control = 0
        if control == 1:                                # checks that W-decay tau+ and neutrinos have progressive numbers 9 and 8
            print 'error mu+/tau+'
    file.Close()

print 'End of negative heavy leptons - 000'

# records the yy*.root files list of the whizard_posMuTau_yyvlyx directory
fileList = glob.glob('./whizard_posMuTau_yyvlyx/001/yy*.root')

for fileName in fileList:
    # reads the yy*.root file
    file = TFile(fileName,"READ")
    tree = file.Get("MyLCTuple")
    
    # loops over the 99 events of the tree
    for event in tree:
        control = 1
        if tree.mcpdg[9] == -13:                        # W-decay muon+ have progressive number 9
            energy = tree.mcene[9]
            px = tree.mcmox[9]
            py = tree.mcmoy[9]
            pz = tree.mcmoz[9]
            cosTheta = pz/sqrt(px**2+py**2+pz**2)
            hPositiveMuon.Fill(energy*red, -cosTheta)
            if tree.mcpdg[8] == 14:                   # relative neutrinos have progressive number 8
                control = 0
        if tree.mcpdg[9] == -15:                        # W-decay tau+ have progressive number 9
            energy = tree.mcene[9]
            px = tree.mcmox[9]
            py = tree.mcmoy[9]
            pz = tree.mcmoz[9]
            cosTheta = pz/sqrt(px**2+py**2+pz**2)
            hPositiveTau.Fill(energy*red, -cosTheta)
            if tree.mcpdg[8] == 16:                   # relative neutrinos have progressive number 8
                control = 0
        if control == 1:                                # checks that W-decay tau+/mu+ and neutrinos have progressive numbers 9 and 8
            print 'error mu+/tau+'
    file.Close()

print 'End of negative heavy leptons - 001'

###########################
### CREATE TOTAL HISTOS ###
###########################

hLightLeptons.Add(hElectron, hPositron)
hMuon.Add(hPositiveMuon, hNegativeMuon)
hTau.Add(hPositiveTau, hNegativeTau)
hPositiveLeptons.Add(hPositron, hPositiveMuon)
hPositiveLeptons.Add(hPositiveTau)
hNegativeLeptons.Add(hElectron, hNegativeMuon)
hNegativeLeptons.Add(hNegativeTau)
hLeptons.Add(hPositiveLeptons, hNegativeLeptons)

######################################################
### saves the histograms in 2DimAllFilesHisto.root ###
######################################################

savingFile = TFile("./2dWhizardLeptonsHisto.root", "CREATE")
hPositron.Write()
hElectron.Write()
hLightLeptons.Write()
hPositiveMuon.Write()
hNegativeMuon.Write()
hMuon.Write()
hPositiveTau.Write()
hNegativeTau.Write()
hTau.Write()
hPositiveLeptons.Write()
hNegativeLeptons.Write()
hLeptons.Write()
savingFile.Close()
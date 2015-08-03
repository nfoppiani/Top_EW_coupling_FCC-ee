from ROOT import TFile, TH2D
import glob
from numpy import sqrt


# REDUCED ENERGY DEFINITION
top = 173.2         # top mass
w = 80.39           # w boson mass
s = 365**2          # center of mass squared energy

beta = sqrt(1-4*top**2/s)               # beta=v/c of the top
r = w**2/top**2
red = 2/top*sqrt((1-beta)/(1+beta))     # reduction factor: REDUCED ENERGY = xf = energy*red
xfMin = r*(1-beta)/(1+beta)             # minimum xf value (maximum is 1)

print 'beta = ', beta
print 'red = ', red
print 'xfMax = 1'
print 'xfMin = ', xfMin


# creates the histograms
hElectron = TH2D("electronEnergyAndAngleHisto", "W-decay electrons energy and cosine of polar angle", 40, 0., 200., 30, -1., 1.)
hElectronReduced = TH2D("electronReducedEnergyAndAngleHisto", "W-decay electrons reduced energy and cosine of polar angle", 40, 0., 1.4, 30, -1., 1.)
hPositron = TH2D("positronEnergyAndAngleHisto", "W-decay positrons energy and cosine of polar angle", 40, 0., 200., 30, -1., 1.)
hPositronReduced = TH2D("electronReducedEnergyAndAngleHisto", "W-decay positrons reduced energy and cosine of polar angle", 40, 0., 1.4, 30, -1., 1.)
hLightLeptons = TH2D("lightLeptonsEnergyAndAngleHisto", "W-decay electrons and positrons energy and cosine of polar angle (multiplied per -1 for positrons)", 40, 0., 200., 30, -1., 1.)
hLightLeptonsReduced = TH2D("lightLeptonsReducedEnergyAndAngleHisto", "W-decay electrons and positrons reduced energy and cosine of polar angle (multiplied per -1 for positrons)", 40, 0., 1.4, 30, -1., 1.)

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
            hPositron.Fill(energy, -cosTheta)                   # cosTheta*(-1) to have the same electrons distribution!
            hPositronReduced.Fill(energy*red, -cosTheta)
            hLightLeptons.Fill(energy, -cosTheta)
            hLightLeptonsReduced.Fill(energy*red, -cosTheta)
            if tree.mcpdg[8] == 12:                             # the relative neutrino has progressive number 8
                control = 0
        if control == 1:                                        # checks that W-decay positrons and neutrinos have progressive numbers 9 and 8
            print 'error'
    file.Close()

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
            hElectron.Fill(energy, cosTheta)
            hElectronReduced.Fill(energy*red, cosTheta)
            hLightLeptons.Fill(energy, cosTheta)
            hLightLeptonsReduced.Fill(energy*red, cosTheta)
            if tree.mcpdg[11] == -12:                   # relative neutrinos have progressive number 11
                control = 0
        if control == 1:                                # checks that W-decay electrons and neutrinos have progressive numbers 10 and 11
            print 'error'
    file.Close()



# saves the histograms in 2DimAllFilesHisto.root
savingFile = TFile("./2dWhizardLightLeptonsHisto.root", "CREATE")
hPositron.Write()
hPositronReduced.Write()
hElectron.Write()
hElectronReduced.Write()
hLightLeptons.Write()
hLightLeptonsReduced.Write()
savingFile.Close()
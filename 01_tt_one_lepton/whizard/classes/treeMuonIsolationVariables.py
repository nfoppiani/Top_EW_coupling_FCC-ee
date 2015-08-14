from ROOT import TFile, TTree, TChain
import numpy
from particleClass import *

# reduced energy definition
top = 174.         # top mass
w = 80.419           # w boson mass
s = 365.**2          # center of mass squared energy

beta = numpy.sqrt(1-4*top**2/s)               # beta=v/c of the top
r = w**2/top**2
red = 2/top*numpy.sqrt((1-beta)/(1+beta))     # reduction factor: REDUCED ENERGY = xf = energy*red
xfMin = r*(1-beta)/(1+beta)             # minimum xf value (maximum is 1)

# print 'beta = ', beta
# print 'red = ', red
# print 'xfMax = 1'
# print 'xfMin = ', xfMin

# records the *ntuple.root files list of the present directory
# this line should stay over electronsTree.root file creation if you replace *ntuple.root with *.root
#fileList = glob.glob("/afs/cern.ch/user/t/tpajero/work/public/whizard_electron_yyxyev/yy*.root")

# chain= TChain("MyLCTuple")
# chain.Add("/afs/cern.ch/user/t/tpajero/work/public/whizard_electron_yyxyev/yy*.root")

# creates the new file and the tree that it will contain
savingFile = TFile("../tree/negMuonsRcTree.root", "CREATE")
muonsRcTree = TTree('negMuons_tree', 'reducedInformationTree')

# defines the arrays needed to fill the tree

#mc muon branch
mcMuEne = numpy.zeros(1, dtype=float,)
mcMuRedEne = numpy.zeros(1, dtype=float,)
mcMuMox = numpy.zeros(1, dtype=float,)
mcMuMoy = numpy.zeros(1, dtype=float,)
mcMuMoz = numpy.zeros(1, dtype=float,)
mcMuCosTheta = numpy.zeros(1, dtype=float,)
mcMuPt = numpy.zeros(1, dtype=float,)

#rc muon branch
rcMuNum = numpy.zeros(6, dtype=float,)
rcMuEne = numpy.zeros(6, dtype=float,)
rcMuRedEne = numpy.zeros(6, dtype=float,)
rcMuMox = numpy.zeros(6, dtype=float,)
rcMuMoy = numpy.zeros(6, dtype=float,)
rcMuMoz = numpy.zeros(6, dtype=float,)
rcMuCosTheta = numpy.zeros(6, dtype=float,)
rcMuPt = numpy.zeros(6, dtype=float,)
rcMuDeltaOneOverPt = numpy.zeros(6, dtype=float,)
rcMuMatch = numpy.zeros(6, dtype=float,)
rcPtToClosestJet = numpy.zeros(6, dtype=float,)
rcAngleClosestCharge = numpy.zeros(6, dtype=float,)
rcenergyInCone = numpy.zeros(6, dtype=float,)

# creates the tree branches

muonsRcTree.Branch('mcMuEne',mcMuEne, 'mcTyp/D')
muonsRcTree.Branch('mcMuRedEne',mcMuRedEne, 'mcTyp/D')
muonsRcTree.Branch('mcMuMox',mcMuMox, 'mcTyp/D')
muonsRcTree.Branch('mcMuMoy',mcMuMoy, 'mcTyp/D')
muonsRcTree.Branch('mcMuMoz',mcMuMoz, 'mcTyp/D')
muonsRcTree.Branch('mcMuCosTheta',mcMuCosTheta, 'mcTyp/D')
muonsRcTree.Branch('mcMuPt',mcMuPt, 'mcTyp/D')

muonsRcTree.Branch('mcMuEne',mcMuEne, 'mcTyp/D')
muonsRcTree.Branch('mcMuEne',mcMuEne, 'mcTyp/D')
muonsRcTree.Branch('mcMuEne',mcMuEne, 'mcTyp/D')
muonsRcTree.Branch('mcMuEne',mcMuEne, 'mcTyp/D')
muonsRcTree.Branch('mcMuEne',mcMuEne, 'mcTyp/D')
muonsRcTree.Branch('mcMuEne',mcMuEne, 'mcTyp/D')
muonsRcTree.Branch('mcMuEne',mcMuEne, 'mcTyp/D')
muonsRcTree.Branch('mcMuEne',mcMuEne, 'mcTyp/D')


for event in chain:
    if tree.mcpdg[10]==13:
        # loops on the particles contained in every event
	
	mcTyp[0] = chain.mcpdg[10]        # prepares the variables to fill the tree
	mcEne[0] = chain.mcene[10]
	mcRedEne[0] = chain.mcene[10]*red
	px = chain.mcmox[10]
	py = chain.mcmoy[10]
	pz = chain.mcmoz[10]
	mcMox[0] = px
	mcMoy[0] = py
	mcMoz[0] = pz
	mcCosTheta[0] = pz/numpy.sqrt(px**2+py**2+pz**2)
	mcInvMas[0] =numpy.sqrt((chain.mcene[2]+chain.mcene[3])**2-(chain.mcmox[2]+chain.mcmox[3])**2-(chain.mcmoy[2]+chain.mcmoy[3])**2-(chain.mcmoz[2]+chain.mcmoz[3])**2)
	
	electronsTree.Fill()        

savingFile.cd()
electronsTree.Write()         # writes the tree in the savingFile
savingFile.Close()

# this program reads the ntuple.root files contained in the present directory, selects from the various events the positive_muons/positive_muons/+-muons coming from a W-decay, and creates a new tree containg their particlePdgID, energy, reduced energy, momenta, cosine of their polar angle, and the mass of the W they decayed from

from ROOT import TFile, TTree, TChain
import numpy

# reduced energy definition
top = 174.         # top mass
w = 80.419           # w boson mass
s = 365.**2          # center of mass squared energy

beta = numpy.sqrt(1-4*top**2/s)               # beta=v/c of the top
r = w**2/top**2
red = 2/top*numpy.sqrt((1-beta)/(1+beta))     # reduction factor: REDUCED ENERGY = xf = energy*red
xfMin = r*(1-beta)/(1+beta)             # minimum xf value (maximum is 1)

print 'beta = ', beta
print 'red = ', red
print 'xfMax = 1'
print 'xfMin = ', xfMin

# records the *ntuple.root files list of the present directory

chain= TChain("MyLCTuple")
chain.Add("/afs/cern.ch/user/t/tpajero/work/public/whizard_posMuTau_yyvlyx/000/yy*.root")
chain.Add("/afs/cern.ch/user/t/tpajero/work/public/whizard_posMuTau_yyvlyx/001/yy*.root")

# creates the new file and the tree that it will contain
savingFile = TFile("../tree/positive_muons_tree.root", "CREATE")
positive_muonsTree = TTree('positive_muons_tree', 'reducedInformationTree')

# defines the arrays needed to fill the tree
mcTyp = numpy.zeros(1, dtype=float,)
mcEne = numpy.zeros(1, dtype=float,)
mcRedEne = numpy.zeros(1, dtype=float,)
mcMox = numpy.zeros(1, dtype=float,)
mcMoy = numpy.zeros(1, dtype=float,)
mcMoz = numpy.zeros(1, dtype=float,)
mcCosTheta = numpy.zeros(1, dtype=float,)
mcInvMas = numpy.zeros(1, dtype=float,)

# creates the tree branches
positive_muonsTree.Branch('mcTyp', mcTyp, 'mcTyp/D')
positive_muonsTree.Branch('mcEne', mcEne, 'mcEne/D')
positive_muonsTree.Branch('mcRedEne', mcRedEne, 'mcRedEne/D')
positive_muonsTree.Branch('mcMox', mcMox, 'mcMox/D')
positive_muonsTree.Branch('mcMoy', mcMoy, 'mcMoy/D')
positive_muonsTree.Branch('mcMoz', mcMoz, 'mcMoz/D')
positive_muonsTree.Branch('mcCosTheta', mcCosTheta, 'mcCosTheta/D')
positive_muonsTree.Branch('mcInvMas', mcInvMas, 'mcInvMas/D')

for event in chain:
	# identifies a particle of the event, varies from 1 to numberOfParticles
	
	# loops on the particles contained in every event
	if chain.mcpdg[9]==-13:
		mcTyp[0] = chain.mcpdg[9]        # prepares the variables to fill the tree
		mcEne[0] = chain.mcene[9]
		mcRedEne[0] = chain.mcene[9]*red
		px = chain.mcmox[9]
		py = chain.mcmoy[9]
		pz = chain.mcmoz[9]
		mcMox[0] = px
		mcMoy[0] = py
		mcMoz[0] = pz
		mcCosTheta[0] = pz/numpy.sqrt(px**2+py**2+pz**2)
		mcInvMas[0] = numpy.sqrt((chain.mcene[2]+chain.mcene[3])**2-(chain.mcmox[2]+chain.mcmox[3])**2-(chain.mcmoy[2]+chain.mcmoy[3])**2-(chain.mcmoz[2]+chain.mcmoz[3])**2)
		
		positive_muonsTree.Fill()        

savingFile.cd()
positive_muonsTree.Write()         # writes the tree in the savingFile
savingFile.Close()

# this program reads the ntuple.root files contained in the present directory, selects from the various events the electrons/positrons/+-muons coming from a W-decay, and creates a new tree containg their particlePdgID, energy, reduced energy, momenta, cosine of their polar angle, and the mass of the W they decayed from

from ROOT import TFile, TTree
import numpy
import glob


# reduced energy definition
top = 173.2         # top mass
w = 80.39           # w boson mass
s = 365**2          # center of mass squared energy

beta = numpy.sqrt(1-4*top**2/s)               # beta=v/c of the top
r = w**2/top**2
red = 2/top*numpy.sqrt((1-beta)/(1+beta))     # reduction factor: REDUCED ENERGY = xf = energy*red
xfMin = r*(1-beta)/(1+beta)             # minimum xf value (maximum is 1)

print 'beta = ', beta
print 'red = ', red
print 'xfMax = 1'
print 'xfMin = ', xfMin

# records the *ntuple.root files list of the present directory
# this line should stay over electronsTree.root file creation if you replace *ntuple.root with *.root
fileList = glob.glob('./*ntuple.root')

# creates the new file and the tree that it will contain
savingFile = TFile("./electrons_Tree.root", "CREATE")
electronsTree = TTree('electrons_Tree', 'reducedInformationTree')

# defines the arrays needed to fill the tree
mcTyp = numpy.zeros(1, dtype=float,)
mcEne = numpy.zeros(1, dtype=float,)
mcRedEne = numpy.zeros(1, dtype=float,)
mcMox = numpy.zeros(1, dtype=float,)
mcMoy = numpy.zeros(1, dtype=float,)
mcMoz = numpy.zeros(1, dtype=float,)
mcCosTheta = numpy.zeros(1, dtype=float,)

# creates the tree branches
electronsTree.Branch('mcTyp', mcTyp, 'mcTyp/D')
electronsTree.Branch('mcEne', mcEne, 'mcEne/D')
electronsTree.Branch('mcRedEne', mcRedEne, 'mcRedEne/D')
electronsTree.Branch('mcMox', mcMox, 'mcMox/D')
electronsTree.Branch('mcMoy', mcMoy, 'mcMoy/D')
electronsTree.Branch('mcMoz', mcMoz, 'mcMoz/D')
electronsTree.Branch('mcCosTheta', mcCosTheta, 'mcCosTheta/D')
electronsTree.Branch('mcWMas', mcWMas, 'mcWMas/D')

for fileName in fileList:
    # reads the ntuple.root file
    file = TFile(fileName,"READ")
    tree = file.Get("MyLCTuple")

    # loops over the 99 events of the tree
    for event in tree:
        # identifies a particle of the event, varies from 1 to numberOfParticles
        
        # loops on the particles contained in every event
        
		mcTyp[0] = tree.mcpdg[10]        # prepares the variables to fill the tree
		mcEne[0] = tree.mcene[10]
		mcRedEne[0] = tree.mcene[10]*red
		px = tree.mcmox[10]
		py = tree.mcmoy[10]
		pz = tree.mcmoz[10]
		mcMox[0] = px
		mcMoy[0] = py
		mcMoz[0] = pz
		mcCosTheta[0] = pz/numpy.sqrt(px**2+py**2+pz**2)
		electronsTree.Fill()        
        

    file.Close()

savingFile.cd()
electronsTree.Write()         # writes the tree in the savingFile
savingFile.Close()

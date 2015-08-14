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

chain= TChain("MyLCTuple")
#chain.Add("/afs/cern.ch/user/t/tpajero/work/public/whizard_electron_yyxyev/yy*.root")
chain.Add('./../ntuple/negMuTau_ntuple/yyxylv_o_*.root')

# creates the new file and the tree that it will contain
savingFile = TFile("../tree/negMuonsRcTree.root", "RECREATE")
muonsRcTree = TTree('negMuons_tree', 'reducedInformationTree')

# defines the arrays needed to fill the tree

# mc muon branch
mcMuEne = numpy.zeros(1, dtype=float,)
mcMuRedEne = numpy.zeros(1, dtype=float,)
mcMuMox = numpy.zeros(1, dtype=float,)
mcMuMoy = numpy.zeros(1, dtype=float,)
mcMuMoz = numpy.zeros(1, dtype=float,)
mcMuTheta = numpy.zeros(1, dtype=float,)
mcMuCosTheta = numpy.zeros(1, dtype=float,)
mcMuPt = numpy.zeros(1, dtype=float,)

#rc muon branch
rcMuNum = numpy.zeros(1, dtype=float,)
rcMuEne = numpy.zeros(1, dtype=float,)
rcMuRedEne = numpy.zeros(1, dtype=float,)
rcMuMox = numpy.zeros(1, dtype=float,)
rcMuMoy = numpy.zeros(1, dtype=float,)
rcMuMoz = numpy.zeros(1, dtype=float,)
rcMuTheta = numpy.zeros(1, dtype=float,)
rcMuPhi = numpy.zeros(1, dtype=float,)
rcMuCosTheta = numpy.zeros(1, dtype=float,)
rcMuPt = numpy.zeros(1, dtype=float,)
rcMuDeltaOneOverPt = numpy.zeros(1, dtype=float,)
rcMuDeltaOneOverPtNorm = numpy.zeros(1, dtype=float,)
rcMuMatch = numpy.zeros(1, dtype=float,)
rcPtToClosestJet = numpy.zeros(1, dtype=float,)
rcEnergyInCone = numpy.zeros(1, dtype=float,)
rcAngleClosestCharge = numpy.zeros(1, dtype=float,)
rcAngleClosestChargeOrNeutron = numpy.zeros(1, dtype=float,)


# creates the tree branches
muonsRcTree.Branch('mcMuEne', mcMuEne, 'mcTyp/D')
muonsRcTree.Branch('mcMuRedEne', mcMuRedEne, 'mcTyp/D')
muonsRcTree.Branch('mcMuMox', mcMuMox, 'mcTyp/D')
muonsRcTree.Branch('mcMuMoy', mcMuMoy, 'mcTyp/D')
muonsRcTree.Branch('mcMuMoz', mcMuMoz, 'mcTyp/D')
muonsRcTree.Branch('mcMuTheta', mcMuTheta, 'mcTyp/D')
muonsRcTree.Branch('mcMuPhi', mcMuPhi, 'mcTyp/D')
muonsRcTree.Branch('mcMuCosTheta', mcMuCosTheta, 'mcTyp/D')
muonsRcTree.Branch('mcMuPt', mcMuPt, 'mcTyp/D')

muonsRcTree.Branch('rcMuNum',rcMuNum, 'mcTyp/D')
muonsRcTree.Branch('rcMuEne',rcMuEne, 'mcTyp/D')
muonsRcTree.Branch('rcMuRedEne',rcMuRedEne, 'mcTyp/D')
muonsRcTree.Branch('rcMuMox',rcMuMox, 'mcTyp/D')
muonsRcTree.Branch('rcMuMoy',rcMuMoy, 'mcTyp/D')
muonsRcTree.Branch('rcMuMoz',rcMuMoz, 'mcTyp/D')
muonsRcTree.Branch('rcMuTheta',rcMuTheta, 'mcTyp/D')
muonsRcTree.Branch('rcMuPhi',rcMuPhi, 'mcTyp/D')
muonsRcTree.Branch('rcMuCosTheta',rcMuCosTheta, 'mcTyp/D')
muonsRcTree.Branch('rcMuPt',rcMuPt, 'mcTyp/D')
muonsRcTree.Branch('rcMuDeltaOneOverPt',rcMuDeltaOneOverPt, 'mcTyp/D')
muonsRcTree.Branch('rcMuDeltaOneOverPtNorm',rcMuDeltaOneOverPtNorm, 'mcTyp/D')
muonsRcTree.Branch('rcMuMatch',rcMuMatch, 'mcTyp/D')
muonsRcTree.Branch('rcPtToClosestJet',rcPtToClosestJet, 'mcTyp/D')
muonsRcTree.Branch('rcEnergyInCone',rcEnergyInCone, 'mcTyp/D')
muonsRcTree.Branch('rcAngleClosestCharge',rcAngleClosestCharge, 'mcTyp/D')
muonsRcTree.Branch('rcAngleClosestChargeOrNeutron',rcAngleClosestChargeOrNeutron, 'mcTyp/D')


# loops on the particles contained in every event
for event in chain:
	if chain.mcpdg[10]==13:
		# prepares the variables to fill the tree

		mcMuon=Particle(10,13,chain.mccha[10],chain.mcmox[10],chain.mcmoy[10],chain.mcmoz[10],chain.mcene[10])

		mcMuEne[0] = mcMuon.p.E()
		mcMuRedEne[0] = mcMuon.p.E()*red
		mcMuMox[0] = mcMuon.p.Px()
		mcMuMoy[0] = mcMuon.p.Py()
		mcMuMoz[0] = mcMuon.p.Pz()
		mcMuTheta[0] = mcMuon.theta()
		mcMuPhi[0] = mcMuon.phi()
		mcMuCosTheta[0] = mcMuon.cosTheta()
		mcMuPt[0] = mcMuon.p.Pt()

		rcParticles=[]
		for i in range(len(chain.rctyp)):
			p = Particle(i, chain.rctyp[i],chain.rccha[i],chain.rcmox[i],chain.rcmoy[i],chain.rcmoz[i],chain.rcene[i])
			rcParticles.append(p)

		rcJets=[]
		for i in range(len(chain.jene)):
			p = Jet(i,chain.jmas[i],chain.jcha[i],chain.jmox[i],chain.jmoy[i],chain.jmoz[i],chain.jene[i])
			rcJets.append(p)

		#find the matched muon

		matchNum=mcMuon.matchMuon(rcParticles)

		for part in rcParticles:
			if part.typ==13:

				rcMuNum[0]=part.num
				rcMuEne[0]=part.p.E()
				rcMuRedEne[0]=part.p.E() * red
				rcMuMox[0]=part.p.Px()
				rcMuMoy[0]=part.p.Py()
				rcMuMoz[0]=part.p.Pz()
				rcMuTheta[0]=part.theta()
				rcMuPhi[0]=part.phi()
				rcMuCosTheta[0]=part.cosTheta()
				rcMuPt[0]=part.p.Pt()
				rcMuDeltaOneOverPt[0]=((1/part.p.Pt())-(1/mcMuon.p.Pt()))
				rcMuDeltaOneOverPtNorm[0] = rcMuDeltaOneOverPt[0]/(1/mcMuon.p.Pt())
				if part.num==matchNum:
					rcMuMatch[0]=1
				else:
					rcMuMatch[0]=0
				rcPtToClosestJet[0]=(part.ptToClosestJet(rcParticles))
				rcEnergyInCone[0]=(part.energyInCone(rcParticles))
				rcAngleClosestCharge[0]=(part.angleToClosestCharge(rcParticles))
				rcAngleClosestChargeOrNeutron[0]=(part.angleToClosestChargeOrNetruon(rcParticles))
				muonsRcTree.Fill()



savingFile.cd()
muonsRcTree.Write()         # writes the tree in the savingFile
savingFile.Close()

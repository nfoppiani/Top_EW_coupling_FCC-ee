from ROOT import TLorentzVector
import numpy

#########################
### PARAMETERS CHOICE ###
#########################

# MATCH PARAMETERS
matchMuonMaxAngleDegrees = 4.5
matchMuonMinEnergy= 10.

# SEARCH PARAMETERS

closestChargeMinEnergy = 0.
energyInConeAngleDegree = 20.

# PHOTON RECOVERY PARAMETERS

anglularRadiusDegrees = 1.5
dthetaDegrees = 0.4
dphiDegrees = 5.5

##########################
### RADIANS CONVERSION ###
##########################

matchMuonMaxAngle = numpy.radians(matchMuonMaxAngleDegrees)
energyInConeAngle = numpy.radians(energyInConeAngleDegree)

angularRadius = numpy.radians(anglularRadiusDegrees)
dtheta = numpy.radians(dthetaDegrees)
dphi = numpy.radians(dphiDegrees)

##########################
### CLASSES DEFINITION ###
##########################

class Particle:

    def __init__ (self,num,typ,cha,px,py,pz,e,status):
        self.num = num
        self.typ = typ
        self.cha = cha
        self.p = TLorentzVector(px,py,pz,e)
        self.status = status

    def energy(self):
        return self.p.E()

    def px(self):
        return self.p.Px()

    def py(self):
        return self.p.Py()

    def pz(self):
        return self.p.Pz()

    def theta(self):
        return self.p.Theta()
    
    def cosTheta(self):
        return self.p.CosTheta()

    def phi(self):
        return self.p.Phi()

    def dtheta(self, part):
        return self.p.Theta() - part.p.Theta()

    def dphi(self, part):
        phiDifference = self.phi()-part.phi()
        if phiDifference > numpy.pi:
            phiDifference -= 2*numpy.pi
        else:
            if phiDifference < -numpy.pi:
                phiDifference += 2*numpy.pi
        return phiDifference

    def angle(self,part2):
        return self.p.Angle(part2.p.Vect())

    def cos(self,part2):
        ang = self.p.Angle(part2.p.Vect())
        return numpy.cos(ang)

### MATCHING AND RECOVERING ###

    def matchMuon(self, listRcPart):
        minAngle = -1.
        rcMuonNumber = -1
        for part in listRcPart:
            if part.typ == 13 and part.p.E()>matchMuonMinEnergy:
                ang = self.angle(part)
                if ang < minAngle or minAngle == -1.:
                    minAngle = ang
                    rcMuonNumber = part.num
        if minAngle < matchMuonMaxAngle:
            return rcMuonNumber
        else:
            return -1

    def photonsRecovery(self, listRcPart):
        for photon in listRcPart:
            if photon.typ == 22 and photon.status:
                thetaDifference = photon.dtheta(self)
                phiDifference = photon.dphi(self)
                if thetaDifference**2+phiDifference**2 < angularRadius**2 or ( abs(thetaDifference)<dtheta and 0<phiDifference<dphi ):
                    #print self.energy()#
                    self.p += photon.p
                    photon.status = 0
                    #print self.energy(), 'recovered2'#
        return


### ISOLATION VARIABLES ###

    def ptToClosestJet(self,jetList):
        angMin = numpy.pi
        pt = -1
        for jet in jetList:
            if jet.cha!=-1 or InvariantMass(self,jet)>11:
                ang = self.angle(jet)
                ptJet = self.p.Pt(jet.p.Vect())
                if ang <= angMin:
                    angMin = ang
                    pt = ptJet
        return pt

    def angleToClosestCharge(self,rcPartList):
        minAng = -1
        for part in rcPartList:
            if part.cha != 0 and part.num != self.num and part.p.E()>closestChargeMinEnergy:
                ang = self.angle(part)
                if ang < minAng or minAng == -1:
                    minAng = ang
        return minAng

    def angleToClosestChargeOrNetruon(self,rcPartList):
        minAng = -1
        for part in rcPartList:
            if (part.cha != 0 or part.typ==2112) and part.p.E()>closestChargeMinEnergy and part.num != self.num:
                ang = self.angle(part)
                if ang < minAng or minAng == -1:
                    minAng = ang
        return minAng

    def angleToClosestParticleNotPhoton(self,rcPartList):
        minAng = -1
        for part in rcPartList:
            if part.p.E()>closestChargeMinEnergy and part.typ != 22 and part.num != self.num:
                ang = self.angle(part)
                if ang < minAng or minAng == -1:
                    minAng = ang
        return minAng

    def energyInCone(self,rcList):
        energy = 0
        for part in rcList:
            if self.angle(part) < energyInConeAngle and self.num!=part.num:
                energy += part.p.E()
        return energy

    def energyChargeInCone(self,rcList):
        energy = 0
        for part in rcList:
            if part.cha != 0 and self.angle(part) < energyInConeAngle and self.num!=part.num:
                energy += part.p.E()
        return energy

    def energyInConeWithoutPhotons(self,rcList):
        energy = 0
        for part in rcList:
            if part.typ != 22 and self.angle(part) < energyInConeAngle and self.num != part.num:
                energy += part.p.E()
        return energy

    def energyChargeInConeNorm(self,rcList):
        energy = 0
        for part in rcList:
            if self.angle(part) < energyInConeAngle and self.num!=part.num and part.cha!=0:
                energy += part.p.E()
        return energy/self.p.E()

### JET CLASS ###

class Jet:

    def __init__ (self,num,mass,cha,px,py,pz,e,status):
        self.num = num
        self.mass = mass
        self.cha = cha
        self.p = TLorentzVector(px,py,pz,e)
        self.status = status

    def energy(self):
        return self.p.E()
    
    def px(self):
        return self.p.Px()
    
    def py(self):
        return self.p.Py()
    
    def pz(self):
        return self.p.Pz()
    
    def theta(self):
        return self.p.Theta()
    
    def cosTheta(self):
        return self.p.CosTheta()
    
    def phi(self):
        return self.p.Phi()
    
    def dtheta(self, part):
        return self.p.Theta() - part.p.Theta()
    
    def dphi(self, part):
        phiDifference = self.phi()-part.phi()
        if phiDifference > numpy.pi:
            phiDifference -= 2*numpy.pi
        else:
            if phiDifference < -numpy.pi:
                phiDifference += 2*numpy.pi
        return phiDifference
    
    def angle(self,part2):
        return self.p.Angle(part2.p.Vect())
    
    def cos(self,part2):
        ang = self.p.Angle(part2.p.Vect())
        return numpy.cos(ang)



### TAGGED JET CLASS ###

class TaggedJet:

    def __init__ (self,num,mass,cha,px,py,pz,e,btag,ctag,status):
        self.num = num
        self.mass = mass
        self.cha = cha
        self.p = TLorentzVector(px,py,pz,e)
        self.btag = btag
        self.ctag = ctag
        self.status = status

    def energy(self):
        return self.p.E()
    
    def px(self):
        return self.p.Px()
    
    def py(self):
        return self.p.Py()
    
    def pz(self):
        return self.p.Pz()
    
    def theta(self):
        return self.p.Theta()
    
    def cosTheta(self):
        return self.p.CosTheta()
    
    def phi(self):
        return self.p.Phi()
    
    def dtheta(self, part):
        return self.p.Theta() - part.p.Theta()
    
    def dphi(self, part):
        phiDifference = self.phi()-part.phi()
        if phiDifference > numpy.pi:
            phiDifference -= 2*numpy.pi
        else:
            if phiDifference < -numpy.pi:
                phiDifference += 2*numpy.pi
        return phiDifference
    
    def angle(self,part):
        return self.p.Angle(part.p.Vect())
    
    def cos(self,part):
        ang = self.p.Angle(part.p.Vect())
        return numpy.cos(ang)

# FUNCTIONS DEFINITION

def Distance(a,b):
    dist = numpy.sqrt((a.p.E()-b.p.E())**2 + (a.p.Px()-b.p.Px())**2 + (a.p.Py()-b.p.Py())**2 + (a.p.Pz()-b.p.Pz())**2)
    return dist

def InvariantMass(a,b):
    return numpy.sqrt((a.energy()-b.energy())**2+(a.px()-b.px())**2+(a.py()-b.py())**2+(a.pz()-b.pz())**2)

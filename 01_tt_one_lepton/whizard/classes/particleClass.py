from ROOT import TLorentzVector
import numpy

#########################
### PARAMETERS CHOICE ###
#########################

# MATCH PARAMETERS
matchMuonMaxAngleDegrees = 5.5
matchMuonMinEnergy= 10.

#matchelectronMinEnergy = 8
matchMinCos = 0.98

# SEARCH PARAMETERS

closestChargeMinEnergy = 2.
closestJetMinEnergy = 5.
energyInConeAngleDegree = 5.

# PHOTON ADDING PARAMETERS

degreeDTheta = 4.0
cosPhiMin = 0.995
photonConeDegreeAngle = 7

##########################
### RADIANS CONVERSION ###
##########################

matchMuonMaxAngle = numpy.radians(matchMuonMaxAngleDegrees)
photonConeAngle = numpy.radians(photonConeDegreeAngle)
dtheta = numpy.radians(degreeDTheta)
energyInConeAngle = numpy.radians(energyInConeAngleDegree)

##########################
### CLASSES DEFINITION ###
##########################

class Particle:

    def __init__ (self,num,typ,cha,px,py,pz,e):
        self.num = num
        self.typ = typ
        self.cha = cha
        self.p = TLorentzVector(px,py,pz,e)
    
    def cosTheta(self):
        return self.p.CosTheta()
    
    def theta(self):
        return self.p.Theta()
    
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

    def ptToClosestJet(self,jetList):
        angMin = numpy.pi
        pt = -1
        for jet in jetList:
            if jet.p.E()>closestJetMinEnergy:
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
    
    def energyInCone(self,rcList):
        energy = 0
        for part in rcList:
            if self.angle(part) < energyInConeAngle and self.num!=part.num:
                energy += part.p.E()
        return energy

    def matchMuon(self, listRcPart):
        minAngle = -1.
        rcMuonNumber = -1
        for part in listRcPart:
            if part.typ == 13: #and part.p.E()>matchMuonMinEnergy:
                ang = self.angle(part)
                if ang < minAngle or minAngle == -1.:
                    minAngle = ang
                    rcMuonNumber = part.num
        if minAngle < matchMuonMaxAngle:
            return rcMuonNumber
        else:
            return -1



####### PHOTONS SUMMING ##########

    def sumPhotonsCone(self,listRcPart):
        if self.typ == 11:
            #print self.p.E()
            for partToAdd in listRcPart:
                if partToAdd.typ == 22:
                    angle = self.angle(partToAdd)
                    if angle < photonConeAngle:
                        self.p += partToAdd.p
                        #print self.p.E()
            #print
        return

    def sumPhotonsRectangle(self, listRcPart):
        if self.typ == 11:
            #print self.p.E()
            elTheta = self.theta()
            elPhi = self.phi()
            for partToAdd in listRcPart:
                if partToAdd.typ == 22:
                    if abs(partToAdd.theta()-elTheta) < dtheta:
                        if numpy.cos(partToAdd.phi() - elPhi) > cosPhiMin and numpy.sin(partToAdd.phi() - elPhi)>0:
                            self.p += partToAdd.p
                            #print self.p.E()
            #print
        return


###### DOES NOT WORK WELL #######
    def matchElectron(self, listRcPart):
        if self.typ == 11:
            minDist = 0
            rcNumber = -1
            for part in listRcPart:
                if part.typ == 11: #and part.p.E() > matchMinEnergy:
                    dist = Distance(self,part)
                    cos = self.cos(part)
                    print cos
                    if dist < minDist or minDist == 0:
                        if cos > matchMinCos:
                            minDist = dist
                            rcNumber = part.num
                            #print 'minimum distance is: ', minDist
            return [rcNumber, minDist]
        return [-1, 0]




class Jet:
    
    def __init__ (self,num,mass,cha,px,py,pz,e):
        self.num = num
        self.mass = mass
        self.cha = cha
        self.p = TLorentzVector(px,py,pz,e)

    def cosTheta(self):
        return self.p.CosTheta()
    
    def angle(self,part2):
        return self.p.Angle(part2.p.Vect())



def Distance(a,b):
    dist = numpy.sqrt((a.p.E()-b.p.E())**2 + (a.p.Px()-b.p.Px())**2 + (a.p.Py()-b.p.Py())**2 + (a.p.Pz()-b.p.Pz())**2)
    return dist

from ROOT import TLorentzVector
import numpy

# PARAMETERS CHOICE

dtheta = 0.04
dphi = 0.04

photonConeDegreeAngle = 10
photonConeAngle = numpy.radians(photonConeDegreeAngle)
print
print 'The photon-acceptance angle is ', photonConeDegreeAngle, 'degrees'

# CLASSES DEFINITION

class Particle:

    def __init__ (self,num,type,cha,px,py,pz,e):
        self.num = num
        self.type = type
        self.cha = cha
        self.p = TLorentzVector(px,py,pz,e)
    
    def cosTheta(self):
        return self.p.CosTheta()
    
    def angle(self,part2):
        return self.p.Angle(part2.p.Vect())
    
    def cos(self,part2):
        ang = self.p.Angle(part2.p.Vect())
        return numpy.cos(ang)
    
    def theta(self):
        return self.p.Theta()
    
    def phi(self):
        return self.p.Phi()
    
    def sumPhotonsCone(self,listRcPart):
        if self.type == 11:
            for partToAdd in listRcPart:
                if partToAdd.type == 22:
                    angle = self.angle(partToAdd)
                    if angle < photonConeAngle:
                        self.p += partToAdd.p
            return

    def sumPhotonsRectangle(self, listRcPart):
        if self.type == 11:
            theta = self.theta()
            phi = self.phi()
            for partToAdd in listRcPart:
                if partToAdd == 22:
                    if abs(partToAdd.theta-theta) < dtheta:
                        if partToAdd.phi > phi-dphi:
                            self.p += partToAdd.p
        return




class Jet:
    
    def __init__ (self,num,mass,px,py,pz,e):
        self.num = num
        self.mass = mass
        self.p = TLorentzVector(px,py,pz,e)

    def cosTheta(self):
        return self.p.CosTheta()
    
    def angle(self,part2):
        return self.p.Angle(part2.p.Vect())



def Distance(a,b):
    dist = numpy.sqrt((a.p.E()-b.p.E())**2 + (a.p.Px()-b.p.Px())**2 + (a.p.Py()-b.p.Py())**2 + (a.p.Pz()-b.p.Pz())**2)
    return dist
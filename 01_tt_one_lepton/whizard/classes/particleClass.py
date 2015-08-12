from ROOT import TLorentzVector
import numpy

# PARAMETERS CHOICE

matchMinEnergy = 8
matchMinCos = 0.9

degreeDTheta = 1.
dtheta = numpy.radians(degreeDTheta)
cosPhiMin = 0.995

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
            #print self.p.E()
            for partToAdd in listRcPart:
                if partToAdd.type == 22:
                    angle = self.angle(partToAdd)
                    if angle < photonConeAngle:
                        self.p += partToAdd.p
                        #print self.p.E()
            print
        return

    def sumPhotonsRectangle(self, listRcPart):
        if self.type == 11:
            print self.p.E()
            elTheta = self.theta()
            elPhi = self.phi()
            for partToAdd in listRcPart:
                if partToAdd.type == 22:
                    if abs(partToAdd.theta()-elTheta) < dtheta:
                        if numpy.cos(partToAdd.phi() - elPhi) > cosPhiMin and numpy.sin(partToAdd.phi() - elPhi)>0:
                            self.p += partToAdd.p
                            print self.p.E()
            print
        return

    def matchElectron(self, listRcPart):
        if self.type == 11:
            minDist = 0
            rcNumber = -1
            for part in listRcPart:
                if part.type == 11: # and part.p.E() > matchMinEnergy:
                    dist = Distance(self,part)
                    cos = self.cos(part)
                    if dist < minDist or minDist == 0:
                        if cos > matchMinCos:
                            minDist = dist
                            rcNumber = part.num
            print 'minimum distance is: ', minDist
            return [rcNumber, minDist]
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
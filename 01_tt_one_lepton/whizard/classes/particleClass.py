from ROOT import TLorentzVector
import numpy

# PARAMETERS CHOICE

matchMuonMaxAngle = 0.04


#matchelectronMinEnergy = 8
matchMinCos = 0.98

degreeDTheta = 4.0
dtheta = numpy.radians(degreeDTheta)
cosPhiMin = 0.995

photonConeDegreeAngle = 7
photonConeAngle = numpy.radians(photonConeDegreeAngle)

# CLASSES DEFINITION

class Particle:

    def __init__ (self,num,type,cha,px,py,pz,e):
        self.num = num
        self.type = type
        self.cha = cha
        self.p = TLorentzVector(px,py,pz,e)
    
    def cosTheta(self):
        return self.p.CosTheta()
    
    def theta(self):
        return self.p.Theta()
    
    def phi(self):
        return self.p.Phi()
    
    def angle(self,part2):
        return self.p.Angle(part2.p.Vect())
    
    def cos(self,part2):
        ang = self.p.Angle(part2.p.Vect())
        return numpy.cos(ang)

    def ptToClosestJet(self,jetList):
        angMin = numpy.pi
        pt = -1
        for jet in jetList:
            ang = self.angle(jet)
            if ang <= angMin:
                angMin = ang
                pt = self.p.Pt(jet.p.Vect())
        return pt
                
    def angleToClosestCharge(self,rcPartList):
        minAng = -1
        for part in rcPartList:
            if part.cha != 0 and part.num != self.num:
                ang = self.angle(part)
                if ang < minAng or minAng == -1:
                    minAng = ang
        return minAng

    def matchMuon(self, listRcPart):
        minAngle = -1.
        rcMuonNumber = -1
        for part in listRcPart:
            if part.type == 13:
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
        if self.type == 11:
            #print self.p.E()
            for partToAdd in listRcPart:
                if partToAdd.type == 22:
                    angle = self.angle(partToAdd)
                    if angle < photonConeAngle:
                        self.p += partToAdd.p
                        #print self.p.E()
            #print
        return

    def sumPhotonsRectangle(self, listRcPart):
        if self.type == 11:
            #print self.p.E()
            elTheta = self.theta()
            elPhi = self.phi()
            for partToAdd in listRcPart:
                if partToAdd.type == 22:
                    if abs(partToAdd.theta()-elTheta) < dtheta:
                        if numpy.cos(partToAdd.phi() - elPhi) > cosPhiMin and numpy.sin(partToAdd.phi() - elPhi)>0:
                            self.p += partToAdd.p
                            #print self.p.E()
            #print
        return


###### DOES NOT WORK WELL #######
    def matchElectron(self, listRcPart):
        if self.type == 11:
            minDist = 0
            rcNumber = -1
            for part in listRcPart:
                if part.type == 11: #and part.p.E() > matchMinEnergy:
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

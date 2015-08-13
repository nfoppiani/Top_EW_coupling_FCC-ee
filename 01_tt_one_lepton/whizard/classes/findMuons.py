import numpy
# requires particleClass.py

# SEARCH PARAMETERS
closestChargeMinEnergy = 2.
coneEnergyAngleDegree = 5.
coneEnergyValue = 10.
closestJetMinEnergy = 5.


degreeDTheta = 4.0
dtheta = numpy.radians(degreeDTheta)
cosPhiMin = 0.995

photonConeDegreeAngle = 7
photonConeAngle = numpy.radians(photonConeDegreeAngle)

coneEnergyAngle = numpy.radians(coneEnergyAngleDegree)
matchMuonMaxAngle = numpy.radians(matchMuonMaxAngleDegrees)


energyCutJets = 10
energyCutCone = 10
energyCutConeEnergy = 10

photonConeDegreeAngle = 10
photonConeAngle = numpy.radians(photonConeDegreeAngle)

coneDegreeAngle = 15
coneAngle = numpy.radians(coneDegreeAngle)

###########################
### pt-based approaches ###
###########################

### 1 ### finds the electron whose minimum pt with respect to the six jets is maximum

def findElectronPtMax(rcList,jetList):
    ptMax = 0               # maximum value of the minimum p_t of an electron with respect to the jets
    number = -1             # RC electron progressive number
    for part in rcList:
        if part.type == 11 and part.p.E() > energyCutJets:
            ptMin = 0
            for jet in jetList:
                pt = part.p.Pt(jet.p.Vect())
                if pt < ptMin or ptMin == 0:
                    ptMin = pt
            if ptMin > ptMax:
                ptMax = ptMin
                number = part.num
    return number

### 2 ### finds the electron whose pt with respect to the closest jet is maximum

def findElectronPtMaxClosestJet(rcList,jetList):
    ptMax = 0
    number = -1
    for part in rcList:
        if part.type == 11 and part.p.E()>energyCutJets:
            angMin = numpy.pi
            pt = 0
            for jet in jetList:
                ang = part.angle(jet)
                if ang <= angMin:
                    angMin = ang
                    pt = part.p.Pt(jet.p.Vect())
            if pt > ptMax:
                ptMax = pt
                number = part.num
    return number

####################################
### cone-based energy approaches ###
####################################

### 3 ### finds the electron whose angle from the closest charged particle is minimum

def findElectronConeChargedParticle(rcList):
    angMax = 0
    number = -1
    for el in rcList:
        if el.type == 11 and el.p.E() > energyCutCone:
            angMin = numpy.pi
            for part in rcList:
                if part.cha != 0:
                    ang = el.angle(part)
                    if ang < angMin:
                        if part.num != el.num:
                            angMin = ang
            if angMin > angMax:
                angMax = angMin
                number = el.num
    return number

def findElectronConeChargedNotElectronParticle(rcList):
    angMax = 0
    number = -1
    for el in rcList:
        if el.type == 11 and el.p.E() > energyCutCone:
            angMin = numpy.pi
            for part in rcList:
                if part.cha != 0 and part.type != 11:
                    ang = el.angle(part)
                    if ang < angMin:
                        if part.num != el.num:
                            angMin = ang
            if angMin > angMax:
                angMax = angMin
                number = el.num
    return number

def findElectronConeChargedNotElectronPositronParticle(rcList):
    angMax = 0
    number = -1
    for el in rcList:
        if el.type == 11 and el.p.E() > energyCutCone:
            angMin = numpy.pi
            for part in rcList:
                if part.cha != 0 and abs(part.type) != 11:
                    ang = el.angle(part)
                    if ang < angMin:
                        if part.num != el.num:
                            angMin = ang
            if angMin > angMax:
                angMax = angMin
                number = el.num
    return number

def findElectronConeParticle(rcList):
    cosMin = 1
    number = -1
    for el in rcList:
        if el.type == 11 and el.p.E() > energyCutCone:
            cosMax = -1
            for part in rcList:
                if part.type != 11 and part.type != 22:
                    ang = el.angle(part)
                    cos = numpy.cos(ang)
                    if cos > cosMax:
                        if part.num != el.num:
                            cosMax = cos
            if cosMax < cosMin:
                cosMin = cosMax
                number = el.num
    return number

####################################
### cone-based energy approaches ###
####################################

### 4 ###

def findElectronConeEnergy(rcList):
    enMin = 0
    number = -1
    for el in rcList:
        if el.type == 11 and el.p.E() > energyCutConeEnergy:
            en = 0
            for part in rcList:
                ang = el.angle(part)
                if ang < coneAngle:
                    if part.type != 22 or ang > photonConeAngle:
                        if part.num != el.num:
                            en += part.p.E()
            if en < enMin or enMin == 0:
                enMin = en
                number = el.num
    return number

def findElectronConeNotElectronPhotonEnergy(rcList):
    enMin = 0
    number = -1
    for el in rcList:
        if el.type == 11 and el.p.E() > energyCutConeEnergy:
            en = 0
            for part in rcList:
                ang = el.angle(part)
                if ang < coneAngle:
                    if part.type != 22 or ang > photonConeAngle:
                        if part.type != 11:
                            en += part.p.E()
            if en < enMin or enMin == 0:
                enMin = en
                number = el.num
    return number
import numpy
# requires particleClass.py

energyCut = 10

def findElectronPtMax(rcList,jetList):
    ptMax = 0
    number = -1
    for part in rcList:
        if part.type == 11 and part.p.E() > energyCut:
            ptMin = 0
            for jet in jetList:
                pt = part.p.Pt(jet.p.Vect())
                if pt < ptMin or ptMin == 0:
                    ptMin = pt
            if ptMin > ptMax:
                ptMax = ptMin
                number = part.num
    return number

'''
# BAD APPROACH (previous is better)
def findElectronJetCos(rcList,jetList):
    cosMin = 1
    number = -1
    for part in rcList:
        if part.type == 11:
            cosMax = -1
            for jet in jetList:
                ang = part.angle(jet)
                cos = numpy.cos(ang)
                if cos > cosMax or cosMax == -1:
                    cosMax = cos
            if cosMax < cosMin:
                cosMin = cosMax
                number = part.num
    return number
'''

photonConeDegreeAngle = 15
photonConeAngle = numpy.radians(photonConeDegreeAngle)

coneDegreeAngle = 10
coneAngle = numpy.radians(coneDegreeAngle)

def findElectronConeEnergy(rcList):
    enMin = 0
    number = -1
    for el in rcList:
        if el.type == 11 and el.p.E() > energyCut:
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

def findElectronConeChargedParticle(rcList):
    cosMin = 1
    number = -1
    for el in rcList:
        if el.type == 11 and el.p.E() > energyCut:
            cosMax = -1
            for part in rcList:
                if part.cha != 0:
                    ang = el.angle(part)
                    cos = numpy.cos(ang)
                    if cos > cosMax:
                        if part.num != el.num:
                            cosMax = cos
            if cosMax < cosMin:
                cosMin = cosMax
                number = el.num
    return number

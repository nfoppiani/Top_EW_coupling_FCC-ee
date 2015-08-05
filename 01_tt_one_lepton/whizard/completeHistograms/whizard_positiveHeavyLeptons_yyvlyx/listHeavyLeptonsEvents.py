from ROOT import TFile
from numpy import sqrt

file = TFile('./yyvlyx_o_1.root',"READ")
tree = file.Get("MyLCTuple")


j = 0

for event in tree:
    w = 0           #
    t = 0           #
    notBoth = 0
    print 'number\tpdgId\tpar0\tpar0n\tpar1\tpar1n\ttdau0\tdau1\tdau2\tdau3\tdau4\tene\t\tmox\t\tmoy\t\tmoz'
    i = 0      # identifies a particle of the event, varies from 1 to numberOfParticles
    # fills the histograms
    for pdgId in tree.mcpdg:
        if abs(tree.mcpdg[i]) == 6:
            t = 1
        if i <50:
            parent0pdg = 0
            parent1pdg = 0
            daughter0pdg = 0
            daughter1pdg = 0
            daughter2pdg = 0
            daughter3pdg = 0
            daughter4pdg = 0
            if tree.mcpdg[i] != 22:
                parent0 = tree.mcpa0[i]
                parent1 = tree.mcpa1[i]
                daughter0 = tree.mcda0[i]
                daughter1 = tree.mcda1[i]
                daughter2 = tree.mcda2[i]
                daughter3 = tree.mcda3[i]
                daughter4 = tree.mcda4[i]
                if parent0 > -1:
                    parent0pdg = tree.mcpdg[parent0]
                if parent1 > -1:
                    parent1pdg = tree.mcpdg[parent1]
                if daughter0 > -1:
                    daughter0pdg = tree.mcpdg[daughter0]
                if daughter1 > -1:
                    daughter1pdg = tree.mcpdg[daughter1]
                if daughter2 > -1:
                    daughter2pdg = tree.mcpdg[daughter2]
                if daughter3 > -1:
                    daughter3pdg = tree.mcpdg[daughter3]
                if daughter4 > -1:
                    daughter4pdg = tree.mcpdg[daughter4]
                print i, '\t', tree.mcpdg[i], '\t', parent0pdg,'\t', parent0, '\t', parent1pdg,'\t', parent1, '\t', daughter0pdg,'\t', daughter1pdg,'\t', daughter2pdg,'\t', daughter3pdg,'\t', daughter4pdg,'\t', tree.mcene[i],'\t', tree.mcmox[i],'\t', tree.mcmoy[i],'\t', tree.mcmoz[i]
        if abs(tree.mcpdg[i]) == 11 and (abs(parent0pdg)==24 or abs(parent1pdg)==24):
            w =1
        i = i+1

    if t == 1 and w != 1:
        notBoth = notBoth +1
    if t != 1 and w == 1:
        notBoth = notBoth +1

    print 'END EVENT ', j, ' ######## ', w, ' ##### ', t
    print
    j = j+1

print 'There are ', notBoth, ' events with only one between (a w which decays in a lepton) and (a top or an antitop).'
# reads a ntuple.root file produced with 'Marlin' instruction from a .slcio file, and writes the energy and momentum of all the particles

from ROOT import TFile

file = TFile("tt_rec_5485_1_ntuple.root","READ")
tree = file.Get("MyLCTuple")

iev = 0
for event in tree:
    print 'Event ',iev
    iev = iev + 1
    ip = 0
    for pdgId in tree.mcpdg:
        e = tree.mcene[ip]
        px = tree.mcmox[ip]
        py = tree.mcmoy[ip]
        pz = tree.mcmoz[ip]
        print ip,pdgId,px,py,pz,e
        ip = ip+1
    print
file.Close()

# line 18 prints the progressive number of the particle in the event, its identification code, its momenta and energy
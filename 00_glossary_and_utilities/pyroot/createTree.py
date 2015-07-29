import ROOT
import numpy

print "Writing a tree"

f = ROOT.TFile("tree.root", "recreate")
t = ROOT.TTree("name_of_tree", "tree title")


# create 1 dimensional float arrays filled with zeroes (python's float datatype corresponds to c++ doubles)
# as fill variables
# filling a tree requires the data to fill to be stored in float array variables (doesn't work with int)!!

n = numpy.zeros(1, dtype=float, )
u = numpy.zeros(1, dtype=float, )

# create the branches and assign the fill-variables to them
# the last argument MUST end with /D
t.Branch('normal', n, 'normal/D')
t.Branch('uniform', u, 'uniform/D')

# create some random numbers, fill them into the fill varibles and call Fill()
for i in xrange(1000):              # from 0 to 999
    n[0] = i
    u[0] = i+0.1
    t.Fill()

# fills the tree with integer numbers in the first column and the same numbers plus 0.1 in the second

# write the tree into the output file and close the file
t.Write()
f.Close()
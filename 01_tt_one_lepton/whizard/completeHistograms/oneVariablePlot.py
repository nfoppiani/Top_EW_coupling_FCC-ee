# This program creates a histo which plots the likelihood as funcion of a

from ROOT import TFile, TH2F, TH1F
import numpy

# MAXIMUM VALUES SETTING
xMax = 177      # number of bins considered for the reduced energy          #####
cosMax = 10     # number of bins to exclude near +-1                        #####
nBin = 200      # a-sample of the likelihood                                #####

# getting the analytic histograms

myfile_an = TFile("SMCrossWhizard364.root","READ")

h_S0 = myfile_an.Get("smcross")
h_f1 = myfile_an.Get("FAzed")                                               #####

#getting the montecarlo histogram

myfile_mc = TFile("2dWhizardLeptons200Histo.root","READ")
electronHisto = myfile_mc.Get("electronReducedEnergyAndAngleHisto")

likeHisto = TH1F("likelihood", "Likelihood as function of a", nBin, 0, 0.012)  #####

N = numpy.zeros((200,200))
S0= numpy.zeros((200,200))
f1= numpy.zeros((200,200))

S0tot = 0.
f1tot = 0.
Ntot = 0.

# putting the data in local variables
# i = 0 is underflow
# j = 0 is overflow

for i in range(200):
    for j in range(200):
        N[i,j]=electronHisto.GetBinContent(i+1,j+1)
        S0[i,j]=h_S0.GetBinContent(i+1,j+1)
        f1[i,j]=h_f1.GetBinContent(i+1,j+1)
        if i < xMax and (j>=cosMax and j<200-cosMax):
            S0tot += S0[i,j]
            f1tot += f1[i,j]
            Ntot += N[i,j]

print 'SM histo normalization factor is: ', S0tot
print 'f1 histo normalization factor is: ', f1tot

def likelihood(a):
    like = 0
    for i in range(xMax):
        for j in range(cosMax,200-cosMax):
            if (S0[i,j]+a*f1[i,j]) > 0:
                like -= N[i,j]*numpy.log(S0[i,j]+a*f1[i,j])
            else:
                print 'error'
                return 0
    like += Ntot*numpy.log(S0tot+a*f1tot)
    like += a**2*f1tot**2*Ntot/2/S0tot/(S0tot+a*f1tot)
    like += 1/2*numpy.log((S0tot+a*f1tot)/S0tot)
    return like

# plotting the histogram

for k in range(nBin):
    a = (k + 0.5)/nBin/80                                                  #####
    aLike = likelihood(a)
    print a, '\t', aLike
    likeHisto.Fill(a, aLike - 590370)
    # next lines only if you want to consider negative values (also change the histo definition!)
    #aLike = likelihood(-a)                                                 #####
    #print -a, '\t', aLike                                                  #####
    #likeHisto.Fill(-a, aLike - 594000)                                     #####

savingFile = TFile("./oneVariablePlot.root", "CREATE")
likeHisto.Write()
savingFile.Close()
from ROOT import TFile, TH2F, TH1F
import numpy

# a = 0.015 +- 0.003
# -0.75

# MAXIMUM VALUES SETTING
xMax = 180      # number of bins
cosMax = 10     # number of bins to exclude near +-1
nBin = 30

# getting the analytic histograms

myfile_an = TFile("../analytic/SMCrossWhizard364.root","READ")

h_S0 = myfile_an.Get("smcross")
h_f1 = myfile_an.Get("FAzed")
h_f2 = myfile_an.Get("FBzed")

#getting the montecarlo histogram

myfile_mc = TFile("../plot/electrons_histo.root","READ")
electronHisto = myfile_mc.Get("mc_electrons")

likeHisto = TH2F("likelihood", "Likelihood as funcion of a", nBin, 0., 0.01,nBin,-0.1,0.)

N = numpy.zeros((200,200))
S0= numpy.zeros((200,200))
f1= numpy.zeros((200,200))
f2= numpy.zeros((200,200)) 

S0tot = 0.
f1tot = 0.
f2tot = 0.
Ntot = 0.


# putting the data in local variables
# i = 0 is underflow
# j = 0 is overflow

for i in range(200):
    for j in range(200):
        
        N[i,j]=electronHisto.GetBinContent(i+1,j+1)
        S0[i,j]=h_S0.GetBinContent(i+1,j+1)
        f1[i,j]=h_f1.GetBinContent(i+1,j+1)
        f2[i,j]=h_f2.GetBinContent(i+1,j+1)
        if i < xMax and (j>=cosMax and j<200-cosMax):
            S0tot += S0[i,j]
            f1tot += f1[i,j]
            f2tot += f2[i,j]
            Ntot += N[i,j]

print 'SM histo normalization factor is: ', S0tot
print 'f1 histo normalization factor is: ', f1tot
print 'f2 histo normalization factor is: ', f2tot

def likelihood(a1,a2):
    like = 0
    for i in range(xMax):
        for j in range(cosMax,200-cosMax):
            if (S0[i,j]+a1*f1[i,j]+a2*f2[i,j]) > 0:
                like -= N[i,j]*numpy.log(S0[i,j]+a1*f1[i,j]+a2*f2[i,j])
            else:
                return 0
    like += Ntot*numpy.log(S0tot + a1*f1tot + a2*f2tot)
    like += (a1*f1tot + a2*f2tot)**2*Ntot/2/S0tot/(S0tot + a1*f1tot + a2*f2tot)
    like += 1/2*numpy.log((S0tot + a1*f1tot + a2*f2tot)/S0tot)
    return like

for k in range(nBin):
	for j in range(nBin):
		a1 = (k + 0.5)/nBin/100
		a2 = (j + 0.5)/nBin/100
		aLike = likelihood(a1,a2)
		print a1,a2, '\t', aLike
		likeHisto.Fill(a1,a2, aLike)

likeHisto.Draw()


#savingFile = TFile("./plotOneVariable.root", "CREATE")
#likeHisto.Write()
#savingFile.Close()

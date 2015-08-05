from ROOT import TFile, TCanvas, TH2F, TH1F
import numpy
from math import log

#getting the analytic histograms

myfile_an = TFile("../analytic/Histo_S0_f1_SM.root","READ")

h_S0 = myfile_an.Get("smcross")
h_f1 = myfile_an.Get("FAzed")

#integral= h_S0.Integral()
#h_S0.Scale(1/integral)
#h_f1.Scale(1/integral)
S0integral=h_S0.Integral()
f1integral=h_f1.Integral()

#getting the montecarlo histogram

myfile_mc = TFile("../plot/electrons_histo.root","READ")

h_mc = myfile_mc.Get("mc_electrons")

N = numpy.zeros((200,200))

S0= numpy.zeros((200,200))

f1= numpy.zeros((200,200))

for i in range(200):
		for j in range(200):
			
			N[i,j]=h_mc.GetBinContent(i+1,j+1)
			S0[i,j]=h_S0.GetBinContent(i+1,j+1)
			f1[i,j]=h_f1.GetBinContent(i+1,j+1)
			if S0[i,j]==0:
				print "error, i,j=", i, j
			if f1[i,j]==0:
				print "error, i,j=", i, j
				
def likelihood(a):
	like = 0.
	for i in range(200):
		for j in range(200):
			if S0[i,j]+a*f1[i,j]<0.:
				print a, S0[i,j]+a*f1[i,j]
				return 0.
			else:
				like=like-N[i,j]*log((S0[i,j]+a*f1[i,j])/(S0integral+a*f1integral))
	return like

h_like=TH1F("likelihood","likelihood",100,-1.,1.)

for b in range(100):
	a=(float(b)+0.5-50)/500
	h_like.Fill(a,likelihood(a))

h_like.Draw()
	

	

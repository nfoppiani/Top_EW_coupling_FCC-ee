from ROOT import TFile, TCanvas, TH2F
import numpy

#getting the analytic histograms

myfile_an = TFile("../analytic/Histo_S0_f1_SM.root","READ")

h_S0=TH2F(" "," ",200,0.112426,1.,200,-1.,1.)
h_f1=TH2F(" "," ",200,0.112426,1.,200,-1.,1.)

h_S0 = myfile_an.Get("smcross")
h_f1 = myfile_an.Get("FAzed")

#getting the montecarlo histogram

myfile_mc = TFile("../plot/2dWhizardPositronHisto.root","READ")

h_mc=TH2F(" "," ",200,0.112426,1.,200,-1.,1.)

h_mc = myfile_mc.Get("electronReducedEnergyAndAngleHisto")

#routines which calculate the minimum

N = numpy.zeroes((200,200))

S0= numpy.zeroes((200,200))

f1= numpy.zeroes((200,200))

for i in range(0,200):
		for j in range(0,200):
			
			N[i,j]=h_mc.GetBinContent(i,j)
			S0[i,j]=h_S0.GetBinContent(i,j)
			f1[i,j]=h_f1.GetBinContent(i,j)
			
a=0.1

iter=0

for iter in range(0,5)
	for i in range(0,200):
		for j in range(0,200):
			
			first_der=first_der - N*f_1/(S_0+a*f_1)
			
			second_der=second_der + N*(f_1/(S_0+a*f_1))**2
	
			a = a + first_der/second_der
			
	print "iteration", iter, "a value", a
	
#calculation of the errors

for iter in range(0,5)
	for i in range(0,200):
		for j in range(0,200):
						
			second_der=second_der + N*(f_1/(S_0+a*f_1))**2

delta_a= numpy.sqrt(1/second_der)

#printing the results

print "a=",a
print
print "delta a =", delta_a

from ROOT import TFile, TCanvas, TH2F
import numpy

#getting the analytic histograms

myfile_an = TFile("../analytic/Histo_S0_f1_SM.root","READ")

h_S0 = myfile_an.Get("smcross")
h_f1 = myfile_an.Get("FAzed")

h_S0.Scale(1/h_S0.Integral())
h_f1.Scale(1/h_S0.Integral())

#getting the montecarlo histogram

myfile_mc = TFile("../plot/electrons_histo.root","READ")

h_mc = myfile_mc.Get("mc_electrons")

#routines which calculate the minimum

N = numpy.zeros((200,200))

S0= numpy.zeros((200,200))

f1= numpy.zeros((200,200))

for i in range(200):
		for j in range(200):
			
			N[i,j]=h_mc.GetBinContent(i,j)
			S0[i,j]=h_S0.GetBinContent(i,j)
			f1[i,j]=h_f1.GetBinContent(i,j)
			
a=0.1

iter=0

for iter in range(5):
	first_der=0
	second_der=0
	for i in range(200):
		for j in range(200):
			
			first_der=first_der - N[i,j]*f1[i,j]/(0.0000001+S0[i,j]+a*f1[i,j])
			
			second_der=second_der + N[i,j]*(f1[i,j]/(0.0000001+S0[i,j]+a*f1[i,j]))**2
			
			a = a - first_der/(second_der+0.0000001)
			
	print "iteration", iter, "a value", a, first_der, second_der
	
#calculation of the errors

second_der=0
for i in range(200):
	for j in range(200):
		second_der=second_der + N[i,j]*(f1[i,j]/(0.0000001+S0[i,j]+a*f1[i,j]))**2

delta_a= numpy.sqrt(1/(second_der+0.0000001))

#printing the results

print "a=",a
print
print "delta a =", delta_a

from ROOT import TFile, TCanvas, TH2F, TF1
import numpy

#getting the analytic histograms

myfile_an = TFile("../analytic/Histo_S0_f1_SM.root","READ")

h_S0 = myfile_an.Get("smcross")
h_f1 = myfile_an.Get("FAzed")

#h_S0.Scale(1/h_S0.Integral())
#h_f1.Scale(1/h_f1.Integral())

#getting the montecarlo histogram

myfile_mc = TFile("../plot/electrons_histo.root","READ")

h_mc = myfile_mc.Get("mc_electrons")

#h_mc.Scale(1/h_mc.Integral())

#routines which calculate the minimum

N = numpy.zeros((200,200))

S0= numpy.zeros((200,200))

f1= numpy.zeros((200,200))

for i in range(200):
		for j in range(200):
			
			N[i,j]=h_mc.GetBinContent(i+1,j+1)
			S0[i,j]=h_S0.GetBinContent(i+1,j+1)
			f1[i,j]=h_f1.GetBinContent(i+1,j+1)
			#if S0[i,j]==0:
				#print i,j,"S0", S0[i,j]
				#print
			#if f1[i,j]==0:
				#print i,j,"f1", f1[i,j]
				#print
a=0.01

iter=0

for iter in range(20):
	first_der=0
	second_der=0
	for i in range(200):
		for j in range(200):
			
			first_der=first_der - N[i,j]*f1[i,j]/(S0[i,j]+a*f1[i,j])
			#first_der = first_der - N[i,j]/((S0[i,j]/f1[i,j])+a)
			second_der=second_der + N[i,j]*(f1[i,j]/(S0[i,j]+a*f1[i,j]))**2
			#second_der=second_der + N[i,j]*(1/((S0[i,j]/f1[i,j])+a))**2
			
	a = a - first_der/second_der
			
	print "iteration", iter, "a value", a, first_der, second_der
	
#calculation of the errors

second_der=0
for i in range(1,200):
	for j in range(1,200):
		#second_der=second_der + N[i,j]*(f1[i,j]/(S0[i,j]+a*f1[i,j]))**2

		second_der=second_der + N[i,j]*(1/((S0[i,j]/f1[i,j])+a))**2
		
delta_a= numpy.sqrt(1/(second_der))

#printing the results

print "a=",a
print
print "delta a =", delta_a

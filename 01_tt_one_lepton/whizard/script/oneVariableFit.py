from ROOT import TFile, TH2F
import numpy

# a = 0.015 +- 0.003
# -0.75

# MAXIMUM VALUES SETTING
xMax = 180      # number of bins
cosMax = 10     # number of bins to exclude near +-1

# getting the analytic histograms

myfile_an = TFile("SMCrossWhizard365.root","READ")

h_S0 = myfile_an.Get("smcross")
h_f1 = myfile_an.Get("FAzed")

# h_S0.Scale(1/h_S0.Integral())       # SM cross section is normalized at 1
# h_f1.Scale(1/h_f1.Integral())       # SM correction cross section is normalized at 1

#getting the montecarlo histogram

myfile_mc = TFile("2dWhizardLeptons200Histo.root","READ")
electronHisto = myfile_mc.Get("electronReducedEnergyAndAngleHisto")

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

a=0.1

first_der = 10.
iter = 0

while abs(first_der) > 10**(-11):
    first_der=0
    second_der=0
    for i in range(xMax):
        for j in range(cosMax,200-cosMax):
            first_der -= N[i,j]*f1[i,j]/(S0[i,j]+a*f1[i,j])
            second_der += N[i,j]*(f1[i,j]/(S0[i,j]+a*f1[i,j]))**2
    first_der += Ntot*f1tot/(S0tot+a*f1tot)
    first_der += a*f1tot**2*Ntot/S0tot/(S0tot+a*f1tot)-(a/(S0tot+a*f1tot))**2*Ntot*f1tot**3/2/S0tot
    first_der += 1/2*f1tot/(S0tot+a*f1tot)
    second_der -= Ntot*(f1tot/(S0tot+a*f1tot))**2
    second_der += f1tot**2*Ntot/S0tot/(S0tot+a*f1tot)+a**2/(S0tot+a*f1tot)**3*Ntot*f1tot**4/S0tot-2*a*f1tot**3*Ntot/S0tot/(S0tot+a*f1tot)**2
    second_der -= 1/2*(f1tot/(S0tot+a*f1tot))**2
    iter += 1
    a = a - first_der/second_der

    print 'iteration', iter
    print 'a = ', a
    print 'first derivative = ', first_der
    print 'second derivative = ', second_der
    print
	
# error calculation

second_der=0
for i in range(xMax):
    for j in range(cosMax,200-cosMax):
        second_der += N[i,j]*(f1[i,j]/(S0[i,j]+a*f1[i,j]))**2
second_der -= Ntot*(f1tot/(S0tot+a*f1tot))**2
second_der += f1tot**2*Ntot/S0tot/(S0tot+a*f1tot)+a**2/(S0tot+a*f1tot)**3*Ntot*f1tot**4/S0tot-2*a*f1tot**3*Ntot/S0tot/(S0tot+a*f1tot)**2
second_der -= 1/2*(f1tot/(S0tot+a*f1tot))**2

delta_a= numpy.sqrt(1/(second_der))

#printing the results

print 'FINAL RESULTS'
print 'a = ',a
print 'delta a = ', delta_a
print
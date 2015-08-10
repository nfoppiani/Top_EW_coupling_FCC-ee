from ROOT import TFile, TH2F
import numpy

# a = 0.015 +- 0.003
# -0.75

# MAXIMUM VALUES SETTING
xMax = 180      # number of bins
cosMax = 10     # number of bins to exclude near +-1

# getting the analytic histograms

myfile_an = TFile("../analytic/SMCrossWhizard364.root","READ")

h_S0 = myfile_an.Get("smcross")
h_f1 = myfile_an.Get("FAzed")
h_f2 = myfile_an.Get("FBzed")

# h_S0.Scale(1/h_S0.Integral())       # SM cross section is normalized at 1
# h_f1.Scale(1/h_f1.Integral())       # SM correction cross section is normalized at 1

#getting the montecarlo histogram

myfile_mc = TFile("../plot/2dWhizardLeptons200Histo.root","READ")
electronHisto = myfile_mc.Get("electronReducedEnergyAndAngleHisto")

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

first_der1 = 10.
first_der2 = 10.
iter = 0

alpha=numpy.zeros((2.,2.)) #matrix with the second derivatives
beta= numpy.array([0.,0.]) #vector with the first derivatives
a=numpy.array([0.07,0.1]) #vector of a

while (abs(first_der1)> 10**(-12) or  abs(first_der2)> 10**(-12)):
    first_der1=0.
    first_der2=0.
    
    second_der1=0.
    second_der2=0.
    second_der1_2=0.
    
    for i in range(xMax):
        for j in range(cosMax,200-cosMax):
            first_der1 -= N[i,j]*f1[i,j]/(S0[i,j]+a[0]*f1[i,j]+a[1]*f2[i,j])
            first_der2 -= N[i,j]*f2[i,j]/(S0[i,j]+a[0]*f1[i,j]+a[1]*f2[i,j])
            
            second_der1 += N[i,j]*(f1[i,j]/(S0[i,j]+a[0]*f1[i,j]+a[1]*f2[i,j]))**2
            second_der2 += N[i,j]*(f2[i,j]/(S0[i,j]+a[0]*f1[i,j]+a[1]*f2[i,j]))**2
            second_der1_2 += N[i,j]*f1[i,j]*f2[i,j]*(1/(S0[i,j]+a[0]*f1[i,j]+a[1]*f2[i,j]))**2
            
	aux=S0tot+a[0]*f1tot+a[1]*f2tot
	
	aux2=a[0]*f1tot+a[1]*f2tot
	
    first_der1 += Ntot*f1tot/aux
    first_der2 += Ntot*f2tot/aux
    
    first_der1 += f1tot*aux2*Ntot/S0tot/aux - f1tot*Ntot*aux2**2/2/S0tot/(aux**2)
    first_der2 += f2tot*aux2*Ntot/(S0tot*aux) - f2tot*Ntot*aux2**2/(2*S0tot*aux**2)
    
    first_der1 += 1/2*f1tot/aux
    first_der2 += 1/2*f2tot/aux
    
    beta[0]=first_der1
    beta[1]=first_der2
    
    second_der1 -= Ntot*(f1tot/aux)**2
    second_der2 -= Ntot*(f2tot/aux)**2
    second_der1_2 -= Ntot*f1tot*f2tot*(1/aux)**2
    
    second_der1 += f1tot**2*Ntot/S0tot/aux+f1tot**2*aux2**2*Ntot/aux**3/S0tot-2*f1tot**2*aux2*Ntot/S0tot/aux**2
    second_der1_2 += f1tot*f2tot*Ntot/S0tot/aux+f1tot*f2tot*aux2**2*Ntot/aux**3/S0tot-2*f1tot*f2tot*aux2*Ntot/S0tot/aux**2
    second_der2 += f2tot**2*Ntot/S0tot/aux+f2tot**2*aux2**2*Ntot/aux**3/S0tot-2*f2tot**2*aux2*Ntot/S0tot/aux**2
    
    second_der1 -= 1/2*(f1tot/aux)**2
    second_der2 -= 1/2*(f2tot/aux)**2
    second_der1_2 -= 1/2*f1tot*f2tot*(1/aux)**2
    
    alpha[0,0]=second_der1
    alpha[0,1]=second_der1_2
    alpha[1,0]=second_der1_2
    alpha[1,1]=second_der2
    
    vec_aux=numpy.linalg.solve(alpha,beta)
    #alpha_inv=numpy.linalg.inv(alpha)
    #print "alpha_inv=" ,alpha_inv[0,0],alpha_inv[0,1],alpha_inv[1,0],alpha_inv[1,1]
    #vec_aux=numpy.array([0.,0.])
    
    #vec_aux[0]= alpha_inv[0,0]*beta[0]  + alpha_inv[0,1]*beta[1]
    #vec_aux[1]= alpha_inv[1,0]*beta[0]  + alpha_inv[1,1]*beta[1]
    
    a = a - vec_aux
    
    #a[0] = a[0] - first_der1/second_der1
    #a[1] = a[1] - first_der2/second_der2
    
    iter += 1

    print 'iteration', iter
    print 'a = ', a
    print "beta=", beta
    print 'vec_aux =', vec_aux
    print 'first derivative = ', first_der1, first_der2
    print 'second derivative = ', second_der1,second_der1_2,second_der2
    print
	
# error calculation

second_der1=0.
second_der2=0.
second_der1_2=0.

for i in range(xMax):
    for j in range(cosMax,200-cosMax):
        second_der1 += N[i,j]*(f1[i,j]/(S0[i,j]+a[0]*f1[i,j]+a[1]*f2[i,j]))**2
        second_der2 += N[i,j]*(f2[i,j]/(S0[i,j]+a[0]*f1[i,j]+a[1]*f2[i,j]))**2
        second_der1_2 += N[i,j]*f1[i,j]*f2[i,j]*(1/(S0[i,j]+a[0]*f1[i,j]+a[1]*f2[i,j]))**2
        
aux=S0tot+a[0]*f1tot+a[1]*f2tot
	
aux2=a[0]*f1tot+a[1]*f2tot

second_der1 -= Ntot*(f1tot/aux)**2
second_der2 -= Ntot*(f2tot/aux)**2
second_der1_2 -= Ntot*f1tot*f2tot*(1/aux)**2

second_der1 += f1tot**2*Ntot/(S0tot*aux)+f1tot**2*aux2**2*Ntot/(aux**3*S0tot)-2*f1tot**2*aux2*Ntot/(S0tot*aux**2)
second_der2 += f2tot**2*Ntot/(S0tot*aux)+f2tot**2*aux2**2*Ntot/(aux**3*S0tot)-2*f2tot**2*aux2*Ntot/(S0tot*aux**2)
second_der1_2 += f1tot*f2tot*Ntot/(S0tot*aux)+f1tot*f2tot*aux2**2*Ntot/(aux**3*S0tot)-2*f1tot*f2tot*aux2*Ntot/(S0tot*aux**2)

second_der1 -= 1/2*(f1tot/aux)**2
second_der2 -= 1/2*(f2tot/aux)**2
second_der1_2 -= 1/2*f1tot*f2tot*(1/aux)**2

alpha[0,0]=second_der1
alpha[0,1]=second_der1_2
alpha[1,0]=second_der1_2
alpha[1,1]=second_der2

cova=numpy.linalg.inv(alpha)

#printing the results

print 'FINAL RESULTS'
print 'a = ', a
print 'cova=' 
print cova

print "delta a1 =", numpy.sqrt(cova[0,0])
print "delta a2 =", numpy.sqrt(cova[1,1])

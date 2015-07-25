import numpy
mw=80.4
mt=173.1
energy=182.5
gamma=energy/mt
beta=numpy.sqrt(1-(1/gamma)**2)

E_min=(mw**2/(2*mt))*numpy.sqrt((1-beta)/(1+beta))
print E_min

E_max=(mt/2)*numpy.sqrt((1+beta)/(1-beta))
print E_max



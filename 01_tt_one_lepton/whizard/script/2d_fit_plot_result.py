from ROOT import *
import numpy

#
#definition of minimum point and covariance matrix
#

a=numpy.array([1.,2.])

cova = numpy.array([[9., 2.4], [2.4, 4.]])

#
#getting the eigenvalues and eigenvectors
#

eigenvals, eigenvecs = numpy.linalg.eig(cova)

sigma=numpy.sqrt(eigenvals)

angle = numpy.rad2deg(numpy.arccos(eigenvecs[0, 0]))

#
#declaration of ellipse
#

pr_1_sigma=0.683

k1=numpy.sqrt(-2*numpy.log(1-pr_1_sigma))

ellipse68=TEllipse(a[0],a[1],sigma[0]*k1,sigma[1]*k1,0.,360.,angle)
ellipse68.SetFillStyle(0)

pr_2_sigma=0.955

k2=-2*numpy.log(1-pr_2_sigma)

ellipse95=TEllipse(a[0],a[1],sigma[0]*k2,sigma[1]*k2,0.,360.,angle)
ellipse95.SetFillStyle(0)

#
#drawing the ellipse
#

x=numpy.zeros(100)
y=numpy.zeros(100)

for i in range(100):
	x[i]=(i-50.)*30./100.

xaxis=TGraph(100,x,y)
yaxis=TGraph(100,y,x)

ellipse_canvas = TCanvas("ciao","ciao", 800,800)
ellipse_canvas.Range(-15.,-15.,15.,15.)
ellipse_canvas.cd()


xaxis.Draw()
yaxis.Draw("same")
ellipse68.Draw("same")
ellipse95.Draw("same")

yaxis.GetYaxis().SetLimits(-20.,20.)
axis->SetLimits(0.,5.);      

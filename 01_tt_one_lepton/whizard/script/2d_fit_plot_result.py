from ROOT import *
import numpy

#
#definition of minimum point and covariance matrix
#

a=numpy.array([0.005,-0.08])

cova = numpy.array([[1.5e-05, 2.6e-05], [2.6e-05, 1.16e-03]])

#
#getting the eigenvalues and eigenvectors
#

eigenvals, eigenvecs = numpy.linalg.eig(cova)

sigma=numpy.sqrt(eigenvals)

angle = numpy.rad2deg(numpy.arccos(eigenvecs[0, 0]))

#
#declaration of ellipse
#

#ellipse1sigma=TEllipse(a[0],a[1],sigma[0],sigma[1],0.,360.,angle)
#ellipse1sigma.SetFillStyle(0)


pr_1_sigma=0.683

k1=numpy.sqrt(-2*numpy.log(1-pr_1_sigma))

ellipse68=TEllipse(a[0],a[1],sigma[0]*k1,sigma[1]*k1,0.,360.,angle)
ellipse68.SetFillStyle(0)

pr_2_sigma=0.955

k2=numpy.sqrt(-2*numpy.log(1-pr_2_sigma))

ellipse95=TEllipse(a[0],a[1],sigma[0]*k2,sigma[1]*k2,0.,360.,angle)
ellipse95.SetFillStyle(0)

pr_3_sigma=0.997

k3=numpy.sqrt(-2*numpy.log(1-pr_3_sigma))

ellipse99=TEllipse(a[0],a[1],sigma[0]*k3,sigma[1]*k3,0.,360.,angle)
ellipse99.SetFillStyle(0)

#
#drawing the ellipse
#

x=numpy.array([-0.05,0.05,0.,0.,0.,0.])
y=numpy.array([0.,0.,0.,-0.3,0.,0.3])

gr=TGraph(6,x,y)


ellipse_canvas = TCanvas("ciao","ciao", 800,800)
ellipse_canvas.Range(-0.05,-0.3,0.05,0.3)
ellipse_canvas.cd()


gr.Draw()
#yaxis.Draw()
#ellipse1sigma.Draw()
ellipse68.Draw()
ellipse95.Draw()
ellipse99.Draw()
#yaxis.GetYaxis().SetLimits(-20.,20.)
#axis->SetLimits(0.,5.);      

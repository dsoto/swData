#!/usr/bin/env python

import pylab

x = pylab.arange(0,10,0.1)
y = pylab.sin(x)

for i in range(1,2):
	print i
	plotname = 'ginputTest'+repr(i)+'.pdf'
	# plot and get user input, then close fig
	pylab.figure(1)
	pylab.plot(x,y)
	points = pylab.ginput(i)
	points = pylab.array(points)
	pylab.close(1)
	
	
	points[:,1] = pylab.sin(points[:,0])
	
	pylab.figure(2)
	# replot with chosen points
	pylab.plot(x,y)
	pylab.plot(points[:,0],points[:,1],'ko')
	
	pylab.savefig(plotname)
	pylab.close(2)


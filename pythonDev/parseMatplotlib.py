#!/usr/bin/env python

import matplotlib.pyplot as mpl
import numpy
import glob
import sys
sys.path.append('../roxanne')
import roxanne
import os.path
	
#fileNameList = glob.glob('*.data')

#for fileName in fileNameList:

fileName = 'sws10-ls-155936.data'
baseFileName = os.path.splitext(fileName)
baseFileName = baseFileName[0]
plotFileName = baseFileName + '_parsed.pdf'

fileIn = open(fileName,'r')
roxanne.readDataFileHeader(fileIn)
columnDict = roxanne.readDataFileArray(fileIn)

voltageForceNormal = columnDict['voltageForceNormal']
voltageForceLateral = columnDict['voltageForceLateral']
voltageForceNormal = numpy.array(voltageForceNormal)
voltageForceLateral = numpy.array(voltageForceLateral)

mpl.figure()
mpl.ion()
mpl.plot(voltageForceNormal)
mpl.plot(voltageForceLateral)
mpl.xlabel('Time (ms)')
mpl.ylabel('Piezo Voltage Signal (V)')
mpl.title(baseFileName)
#mpl.show()
	
print 'acceptable?'
response = raw_input()
print response

points = mpl.ginput(3)
points = numpy.array(points)
mpl.plot(points[:,0],points[:,1],'bo')
#mpl.show()

mpl.savefig(plotFileName)
	

# #	points = points[0]
# 	print points
# 	# why won't this plot now???
# 	pylab.figure(1)
# #	pylab.scatter(points,s=1,c='b',marker='o')
# 	pylab.waitforbuttonpress()
# 	pylab.savefig(plotFileName,transparent=True)
# 	pylab.close(1)
# 	return 0
# 	pylab.figure(1)
# 	pylab.plot(x,y)
# 	points = pylab.ginput(i)
# 	points = pylab.array(points)
# 	pylab.close(1)
# 	points[:,1] = pylab.sin(points[:,0])
# 	pylab.figure(2)
# 	pylab.plot(x,y)
# 	pylab.plot(points[:,0],points[:,1],'ko')
# 	pylab.savefig(plotname)
# 	pylab.close(2)

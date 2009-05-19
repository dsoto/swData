#!/usr/bin/env python

# plotting script that expects a header line with labels for 
# each column of data
# these columns of data will be assigned to a dictionary
# returned values are all strings

import sys
sys.path.append('../roxanne')
import roxanne
import numpy as np

def main():
	fileName = 'analyzed.data'
	fileIn = open(fileName,'r')
	columnDict = roxanne.readDataFileArray(fileIn)
	
	shearForce = columnDict['forceMaxShear']
	normalForce = columnDict['forceMaxAdhesion']
	shearForce = np.array(shearForce)
	normalForce = np.array(normalForce)
	
# 	import matplotlib
# 	params = {'font.family': 'serif',
# 	          'font.serif' : 'Computer Modern Roman',
# 	          'text.usetex': True}
# 	matplotlib.rcParams.update(params)
	
	import matplotlib.pyplot
	import matplotlib.axis
	
	
	matplotlib.pyplot.plot(shearForce,normalForce,
									       linestyle = 'None',
									       marker = 'o',
	                       markerfacecolor = 'w',
	                       markeredgecolor = 'g')
	matplotlib.pyplot.xlabel('Shear Force (microNewtons)')
	matplotlib.pyplot.ylabel('Adhesion Force (microNewtons)')
	matplotlib.pyplot.title('sws10 - 529b02 - Limit Surface - 20090225')
	matplotlib.pyplot.grid(True)
	matplotlib.pyplot.axis([0, 10, -5, 0])
	matplotlib.pyplot.savefig('mplLimitSurface.pdf',transparent=True)
#	matplotlib.pyplot.show()

	import os
	os.system('open mplLimitSurface.pdf')

# TODO : format plot with fonts and size

if __name__ == '__main__':
	main()



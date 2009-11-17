#!/usr/bin/env python

# plotting script that expects a header line with labels for 
# each column of data
# these columns of data will be assigned to a dictionary
# returned values are all strings

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
sys.path.append('../../roxanne')
import roxanne
import numpy as np

fileName = 'analyzed.data'
fileIn = open(fileName,'r')
columnDict = roxanne.readDataFileArray(fileIn)

shearForce = columnDict['forceMaxShear']
normalForce = columnDict['forceMaxAdhesion']
pitchAngle = columnDict['anglePitch']
shearForce = np.array(shearForce,dtype=float)
normalForce = np.array(normalForce,dtype=float)

dataDict = {}
for i,a in enumerate(pitchAngle):
    forcePair = [shearForce[i], normalForce[i]]
    if a not in dataDict.keys():
        dataDict[a] = [forcePair]
    else:
        dataDict[a].append(forcePair)

import matplotlib.pyplot as plt

figure = plt.figure()
axes = figure.add_subplot(111)

for k in dataDict.keys():
    d = zip(*dataDict[k])
    # print d
    axes.plot(d[0],d[1],'.',label=k)

axes.legend()
figure.savefig('combined.pdf')
plt.show()

'''
    
    matplotlib.pyplot.plot(shearForce,normalForce,
                                           linestyle = 'None',
                                           marker = 'o',
                           markerfacecolor = 'w',
                           markeredgecolor = 'g')
    matplotlib.pyplot.xlabel('Shear Force (microNewtons)')
    matplotlib.pyplot.ylabel('Adhesion Force (microNewtons)')
    matplotlib.pyplot.title('sws10 - 529b02 - Limit Surface - 20090526')
    matplotlib.pyplot.grid(True)
    matplotlib.pyplot.axis([0, 10, -5, 0])
    matplotlib.pyplot.savefig('mplLimitSurface.pdf',transparent=True)
    #	matplotlib.pyplot.show()
    
    import os
    os.system('open mplLimitSurface.pdf')
'''
# TODO : format plot with fonts and size


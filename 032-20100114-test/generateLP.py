#!/usr/bin/env python

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/code')
import generateTrajectory as gt

import numpy              as np


preload  = [5, 10, 15, 20, 25, 26, 27]
timeStep = 10.0
velocity = [20.0, 20.0]
numZeros = 100

fileName = 'LP-series'

indexFile = open(fileName+'.index','w')
indexHeaderString = 'startIndex' + '\t' + 'endIndex' + '\n'
indexFile.write(indexHeaderString)

traj = gt.trajectory()
traj.setTimeStepMS(timeStep)

for p in preload:
    vertices = np.array([[0, 0],
                         [p, 0],
                         [0, 0]])

    traj.setVertices(vertices)
    traj.setVelocities(velocity)

    startIndex = traj.getPointsLength()

    traj.addTrailingZeros(numZeros)
    traj.createPoints()
    traj.addTrailingZeros(numZeros)

    endIndex = traj.getPointsLength()
    outString = str(startIndex) + '\t' + str(endIndex) + '\n'
    
    print outString
    indexFile.write(outString)
        

indexFile.close()

# save trajectory file
traj.saveTrajectory(fileName+'.traj')


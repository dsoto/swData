#!/usr/bin/env python

import numpy              as np
import sys
sys.path.append('/Users/dsoto/current/swDataFlat/code')
import generateTrajectory as gt


# create filename for trajectory
fileName = 'shearBending-v40-ts05'

# define parameters
X = np.arange(10.0,15.0+1)
Y = [20.0]
velocity = [20.0, 40.0, 40.0, 20.0]
timeStep = 5.0
numZeros = 100

# initialize trajectory object
traj = gt.trajectory()
traj.setTimeStepMS(timeStep)

# open index file
indexFile = open(fileName+'.index','w')

# write index header
indexHeadings = ['startIndex', 'endIndex', 'x', 'y']
separator = '\t'
indexHeaderString = separator.join(indexHeadings)
indexHeaderString += '\n'

# write header string
indexFile.write(indexHeaderString)

# loop through x and y
for x in X:
    for y in Y:
        vertices = np.array(
                   [[0.0, 0.0],
                    [  x, 0.0],
                    [  x,   y],
                    [  x, 0.0],
                    [0.0, 0.0]])
        # set vertices and velocities in object
        traj.setVertices(vertices)
        traj.setVelocities(velocity)
        startIndex = traj.getPointsLength()
        traj.addTrailingZeros(numZeros)
        # render points from vertices and velocities
        traj.createPoints()
        traj.addTrailingZeros(numZeros)
        endIndex = traj.getPointsLength()
        data = [str(startIndex), str(endIndex), str(x), str(y)]
        outString = separator.join(data) + '\n'
        print outString
        indexFile.write(outString)


# plot path xy
# plot path vs time

indexFile.close()
traj.saveTrajectory(fileName+'.traj')

#traj.plotPath('dummy.pdf')
traj.plotPathTimeTrace(fileName)


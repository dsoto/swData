#!/usr/bin/env python

import numpy              as np
import generateTrajectory as gt

formatString = 'LDP-vp%02.0f-vd%02.0f'

preload  = np.linspace(25, 35, 5)
drag     = np.linspace( 0, 10, 11)
timeStep = 10.0
velocity = [20.0, 20.0, 20.0, 100.0]
numZeros = 100

fileName = formatString % (velocity[0],
                           velocity[1])        

indexFile = open(fileName+'.index','w')
indexHeaderString  = 'startIndex'+'\t'
indexHeaderString += 'endIndex'+'\t'
indexHeaderString += 'preload'+'\t'
indexHeaderString += 'drag' + '\n'

indexFile.write(indexHeaderString)

traj = gt.trajectory()
traj.setTimeStepMS(timeStep)

for p in preload:
    for d in drag:
        vertices = np.array([[0, 0],
                             [p, 0],
                             [p, d],
                             [0, d],
                             [0, 0]])

        traj.setVertices(vertices)
        traj.setVelocities(velocity)

        startIndex = traj.getPointsLength()

        traj.addTrailingZeros(numZeros)
        traj.createPoints()
        traj.addTrailingZeros(numZeros)

        endIndex = traj.getPointsLength()
        outString  = str(startIndex) + '\t' 
        outString += str(endIndex)   + '\t' 
        outString += str(p)          + '\t'
        outString += str(d)          + '\n'
        
        print outString
        indexFile.write(outString)

indexFile.close()
traj.plotPath()
# save trajectory file
traj.saveTrajectory(fileName+'.traj')

# save index

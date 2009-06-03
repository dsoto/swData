#!/usr/bin/env python

import numpy              as np
import generateTrajectory as gt

formatString = 'LS_p%02.0f_a%02.0f_v%02.0f_dt%02.0f.traj'
formatString = 'LS_p%02.0f_d%02.0f_vp%02.0f_vd%02.0f'

angleDegree = np.hstack([np.linspace(0,9,10), np.linspace(10,90,9)])
angleRadian = angleDegree * np.pi / 180.0

preload  = [40.0]
drag     = 80.0
timeStep = 10.0
velocity = [20.0, 20.0, 100.0, 100.0]
numZeros = 100

fileName = formatString % (preload[0], 
                           drag, 
                           velocity[0],
                           velocity[1])        

indexFile = open(fileName+'.index','w')
indexHeaderString = 'startIndex'+'\t'+'endIndex'+'\t'+'angle'+'\n'
indexFile.write(indexHeaderString)


traj = gt.trajectory()
traj.setTimeStepMS(timeStep)

for p in preload:
    for i, a in enumerate(angleRadian):
        if (p - drag*np.sin(a) >= 0):
            vertices = np.array(
                       [[0,                  0],
                        [p,                  0],
                        [p - drag*np.sin(a), drag*np.cos(a)],
                        [0,                  drag*np.cos(a)],
                        [0,                  0]])
        else:
            vertices = np.array(
                       [[0,                  0],
                        [p,                  0],
                        [0,                  drag*np.cos(a)],
                        [0,                  drag*np.cos(a)],
                        [0,                  0]])

        traj.setVertices(vertices)
        traj.setVelocities(velocity)

        startIndex = traj.getPointsLength()

        traj.addTrailingZeros(numZeros)
        traj.createPoints()
        traj.addTrailingZeros(numZeros)

        endIndex = traj.getPointsLength()
        outString = str(startIndex) + '\t' + str(endIndex) + '\t' +str(angleDegree[i]) + '\n'
        
        print outString
        indexFile.write(outString)
        
indexFile.close()
#traj.plotPath()
# save trajectory file
traj.saveTrajectory(fileName+'.traj')

# save index

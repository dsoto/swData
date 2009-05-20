#!/usr/bin/env python

import numpy              as np
import generateTrajectory as gt

formatString = 'LS_p%02.0f_a%02.0f_v%02.0f.traj'
startPreload = 30
endPreload = 35

preload = range(startPreload, endPreload+1)

angle = range(0,10)
angleDegree = np.hstack([angle, range(10,100,10)])
angleRadian = angleDegree * np.pi / 180.0

drag = 80
velocity = [20, 20, 100, 100]
numZeros = 50

traj = gt.trajectory()



preload = [30]
#angleRadian = [0]
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
        fileName = formatString % (p, angleDegree[i], velocity[1])

        traj.setVertices(vertices)
        traj.setVelocities(velocity)

        startIndex = traj.getPointsLength()

        traj.addTrailingZeros(numZeros)
        traj.createPoints()
        traj.addTrailingZeros(numZeros)

        endIndex = traj.getPointsLength()
        
        print fileName, startIndex, endIndex
        
        
traj.saveTrajectory('30preload.traj')
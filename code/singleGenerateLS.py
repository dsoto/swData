#!/usr/bin/env python

import numpy              as np
import generateTrajectory as gt

formatString = 'LS_p%02.0f_a%02.0f_v%02.0f.traj'

angleDegree = np.array([0, 45, 90])
angleRadian = angleDegree * np.pi / 180.0

drag = 5
velocity = [1, 1, 1, 1]
numZeros = 5

traj = gt.trajectory()
traj.setTimeStepMS(1000)


preload = [5]
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
#!/usr/bin/env python

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/code')
import generateTrajectory as gt
import numpy as np

drag = np.linspace(5,40,8)
preload = np.linspace(25,35,6)
pauseSeconds = 5
timeStepMS = 10
slow = 20.0
fast = 100.0
numZeros = 100
velocity = [slow, slow, pauseSeconds, slow, fast]

formatString = 'photo-%02dd-%dp.traj'

traj = gt.trajectory()
traj.setTimeStepMS(timeStepMS)
traj.setVelocities(velocity)

for d in drag:
    for p in preload:
        traj.clearPoints()
        vertices = [[0, 0],  # start
                    [p, 0],  # preload
                    [p, d],  # drag
                    [p, d],  # stall
                    [0, d],  # pulloff
                    [0, 0]]  # return to home
        traj.setVertices(vertices)
        traj.printVertices()
        traj.addTrailingZeros(numZeros)
        traj.createPoints()
        traj.addTrailingZeros(numZeros)

        fileName = formatString % (d,p)
        print fileName
        trajFile = open(fileName,'w')
        traj.saveTrajectory(fileName)
        #traj.plotPath('dummy.pdf')
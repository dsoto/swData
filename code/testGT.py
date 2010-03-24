#!/usr/bin/env python

'''
this script tests the ability of the generateTrajectory class
to have a stall point.  that is to hold at one point for a period
of time
'''

import generateTrajectory as gt


traj = gt.trajectory()
traj.setTimeStepMS(1000)
traj.setVelocities((10,10,10))
traj.setVertices(((0,0),(100,100),(100,100),(0,0)))

traj.createPoints()
traj.printPath()
print 'num points = ', traj.getPointsLength()

#!/usr/bin/env python

import numpy as np

class trajectory:

    # time in seconds
    outputTimeStep      =  0.001
    acquisitionTimeStep =  0.001
    xPoints = [0]
    yPoints = [0]

    def __init__(self):
        pass

    def plotPath(self, fileName):
        print 'plot'
        import matplotlib.pyplot as plt
        plt.plot(self.xPoints, self.yPoints)
        plt.show()
        #plt.savefig(fileName + '.pdf')

    def plotPathTimeTrace(self, fileName):
        import matplotlib.pyplot as plt
        plt.plot(self.xPoints,label='x')
        plt.plot(self.yPoints,label='y')
        plt.legend()
        plt.show()

    def printPath(self):
        for this in zip(self.xPoints, self.yPoints):
            print "x = %.1f,  y = %.1f" % (this[0],this[1])

    def saveTrajectory(self, fileName):
        fOut = open(fileName,'w')
        outString = '%.2f\t%.2f\n' % (self.outputTimeStep*1000,
                                      self.acquisitionTimeStep*1000)
        fOut.write(outString)
        for this in zip(self.xPoints, self.yPoints):
            outString = '%.2f\t%.2f\n' % (this[0], this[1])
            fOut.write(outString)


    def setTimeStepMS(self, timeStep):
        self.outputTimeStep = timeStep / 1000.0
        self.acquisitionTimeStep = timeStep / 1000.0

    def setVertices(self,vertices):
        # takes list or np.array
        # converts to array
        # stores as member variable
        self.vertices = np.array(vertices)

    def setVelocities(self, velocities):
        # if the distance of one of the legs is zero
        # the velocity is interpreted as the time between
        # the two points
        self.velocities = np.array(velocities,dtype=float)

    def printVertices(self):
        for pair in self.vertices:
            print 'x = ' + str(pair[0]) + ', y = ' + str(pair[1])

    def printVelocities(self):
        for velocity in self.velocities:
            print velocity

    def createPoints(self):
        # numLegs is number of vertices - 1
        numLegs = self.vertices.shape[0] - 1
        for i in range(numLegs):
            distance = np.linalg.norm(self.vertices[i] -
                                      self.vertices[i+1])
            #if distance = 0 velocity interpreted as time
            if (distance == 0):
                numSteps = np.floor(self.velocities[i]/self.outputTimeStep)
            else:
                numSteps = np.floor(distance/self.velocities[i]/self.outputTimeStep)
            xLeg = np.linspace(self.vertices[i,   0],
                               self.vertices[i+1, 0],
                               numSteps+1)
            yLeg = np.linspace(self.vertices[i,   1],
                               self.vertices[i+1, 1],
                               numSteps+1)
            self.xPoints = np.hstack([self.xPoints[0:-1], xLeg])
            self.yPoints = np.hstack([self.yPoints[0:-1], yLeg])


    def clearPoints(self):
        self.xPoints = [0]
        self.yPoints = [0]

    def addBeginningZeros(self, numZeros):
         # prepend points with beginning zeros
        self.xPoints = np.hstack([np.zeros(numZeros),self.xPoints])
        self.yPoints = np.hstack([np.zeros(numZeros),self.yPoints])

    def addTrailingZeros(self, numZeros):
        # append points with trailing zeros
        self.xPoints = np.hstack([self.xPoints,np.zeros(numZeros)])
        self.yPoints = np.hstack([self.yPoints,np.zeros(numZeros)])

    def getPointsLength(self):
        return len(self.xPoints)

def main():
    print 'generateTrajectory.py main running'
    traj = trajectory()
    traj.setVertices([[0,0],[1,0],[1,1],[0,0]])
    traj.setVelocities([0.5,0.5,0.5])
    traj.createPoints()
    traj.printPath()
    print traj.getPointsLength()
    #traj.clearPoints()
    #traj.printPath()
    traj.createPoints()
    #traj.addBeginningZeros(2)
    #traj.addTrailingZeros(2)
    traj.printPath()
    #traj.saveTrajectory('trajectory.traj')
    print traj.getPointsLength()

if __name__ == '__main__':
    main()

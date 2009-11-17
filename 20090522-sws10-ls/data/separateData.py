#!/usr/bin/env python

import sys
sys.path.append('../roxanne/')
sys.path.append('../../roxanne/')
import roxanne as rx


def convertTime(data):
    timeStrings = data['time']
    timeSeconds = [float(ts[0:2])*3600+float(ts[3:5])*60+float(ts[6:]) for ts in timeStrings]
    
    import numpy as np
    timeSeconds = np.array(timeSeconds)
    timeSeconds = timeSeconds - timeSeconds[0]
    data['time'] = map(str,timeSeconds)


def getHeader(fileIn):
    # loop through header and return header in string
    header = []
    keepReading = 1
    while keepReading == 1:
        tempLine = fileIn.readline()
        tempLine = tempLine.strip()
        header.append(tempLine)    
        if tempLine.find('<data>') != -1:
            keepReading = 0
    return header


fileIn = open('ls_sws10_20090522_162401.data')
fileIndex = open('indexFile.index')
header = getHeader(fileIn)
#print header
# read in dictionary
data = rx.readDataFileArray(fileIn)
convertTime(data)
# zip into list of tuples
data = zip(data['time'],
           data['voltageForceLateral'],
           data['voltageForceNormal'],
           data['voltagePositionX'],
           data['voltagePositionY'])


index = rx.readDataFileArray(fileIndex)
index['angle'] = [str(round(float(a),0)) for a in index['angle']]
index = zip(map(int,(index['startIndex'])),
            map(int,(index['endIndex'])),
            index['angle'])


numFiles = len(index)
for i in range(numFiles):
    fileOut = open('a%02s.data' % index[i][2],'w')
    fileOut.write('\n'.join(header))
    fileOut.write('\n')
    fileOut.write('time\tvoltageForceLateral\tvoltageForceNormal\tvoltagePositionX\tvoltagePositionY\n')

    for j in range(index[i][0], index[i][1]):
        outString = '\t'.join(data[j])
        fileOut.write(outString)
        fileOut.write('\n')
    #fileNameOut = '%s.data' % index['angle'][i]
    #fileOut = open(fileNameOut,'w')
    




    
'''
import matplotlib.pyplot as plt

def plotTime(fileIn):
    rx.readDataFileHeader(fileIn)
    data = rx.readDataFileArray(fileIn)
    
    timeStrings = data['time']
    
    timeSeconds = [float(ts[0:2])*3600+float(ts[3:5])*60+float(ts[6:]) for ts in timeStrings]
    
    import numpy as np
    timeSeconds = np.array(timeSeconds)
    timeSeconds = timeSeconds - timeSeconds[0]
    
    #print timeSeconds
    
    plt.plot(timeSeconds,'o')

import glob
fileNameList = glob.glob('*.data')
for fileName in fileNameList:
    fileIn = open(fileName)
    plotTime(fileIn)

import numpy as np
x = np.array(range(6000))
y = x * 0.010
y1 = x * 0.005
y2 = x * 0.002
y3 = x * 0.001

plt.plot(x,y)
plt.plot(x,y1)
plt.plot(x,y2)
plt.plot(x,y3)

plt.show()
    
'''
#!/usr/bin/env python
'''
arg 1 : batch data file
arg 2 : index file
arg 3 : prefix
'''

''' 
fixme - files currently placed in /raw, instead place in /separated
fixme - zero out timestamp in each separated file
'''

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne/')
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


# get data file
#fileIn = open(sys.argv[1])
fileInFull = sys.argv[1]
# pull apart fileIn to get place to save files
import os.path
fileInPath = os.path.split(fileInFull)[0]
fileIn = open(fileInFull)

# get index file
fileIndex = open(sys.argv[2])
# get file prefix
prefix = sys.argv[3]

header = getHeader(fileIn)
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
index['angle'] = [('%02.0f' % float(a)) for a in index['angle']]
index = zip(map(int,(index['startIndex'])),
            map(int,(index['endIndex'])),
            index['angle'])


numFiles = len(index)
for i in range(numFiles):
    fileOutPath = fileInPath
    fileOutName = prefix + 'a%s.data' % index[i][2]
    fileOutName = os.path.join(fileOutPath, fileOutName)
    print 'writing ' + fileOutName
    fileOut = open(fileOutName,'w')
    fileOut.write('\n'.join(header))
    fileOut.write('\n')
    fileOut.write('time\tvoltageForceLateral\tvoltageForceNormal\tvoltagePositionX\tvoltagePositionY\n')

    for j in range(index[i][0], index[i][1]):
        outString = '\t'.join(data[j])
        fileOut.write(outString)
        fileOut.write('\n')
    #fileNameOut = '%s.data' % index['angle'][i]
    #fileOut = open(fileNameOut,'w')
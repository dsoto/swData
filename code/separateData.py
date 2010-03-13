#!/usr/bin/env python

# file to separate data file and convert to force and micron data
import roxanne as rx
import numpy as np

# this function should be in roxanne
def getHeader(fileIn):
    # loop through header and return header in dictionary
    # if line has equals sign put lhs of equals as string for dict key
    # and put rhs as value
    header = {}
    keepReading = 1
    while keepReading == 1:
        tempLine = fileIn.readline()
        if tempLine.find('=') != -1:
            (key,value) = tempLine.split('=')
            key = key.strip()
            value = value.strip()
            header[key] = value
        if tempLine.find('<data>') != -1:
            keepReading = 0
    return header

def outputDictAsText(dict, fileOut):
    for key in dict.keys():
        fileOut.write(key + ' = ' + str(dict[key])+ '\n')

def outputDictAsTextByIndex(dict, i, fileOut):
    newDict = {}
    for key in dict.keys():
        newDict[key]=dict[key][i]
    outputDictAsText(newDict, fileOut)

def convertTime(timeStrings):
    timeStrings = data['time']
    timeSeconds = [float(ts[0:2])*3600+float(ts[3:5])*60+float(ts[6:]) for ts in timeStrings]
    timeSeconds = np.array(timeSeconds)
    timeSeconds = timeSeconds - timeSeconds[0]
    timeSeconds = map(str,timeSeconds)
    return timeSeconds

def convertData(data, cantileverDict):
    # convert time to list of floats
    data['time'] = convertTime(data['time'])

    # convert all lists to numpy arrays for ease of manipulation
    #keys = data.keys()
    for key in data.keys():
        data[key] = np.array(data[key],dtype=float)


    # make conversions
    data['positionLateralMicron'] = data['voltagePositionY']*10.0
    data['positionNormalMicron']  = data['voltagePositionX']*10.0

    # cantilever stiffnesses in newtons per meter
    normalStiffness      = cantileverDict['normalStiffness']
    lateralStiffness     = cantileverDict['lateralStiffness']
    # displacement sensitivity measured at 100x amplification
    normalDisplacement   = cantileverDict['normalDisplacement']
    lateralDisplacement  = cantileverDict['lateralDisplacement']

    # use cantilever values to convert voltages to forces
    data['forceLateralMicroNewton'] = (data['voltageForceLateral'] *
                                       lateralStiffness / lateralDisplacement)
    data['forceNormalMicroNewton']  = (data['voltageForceNormal'] *
                                       normalStiffness / normalDisplacement)
    # make polarity adjustments
    data['forceLateralMicroNewton'] *= -1

    return data


'''raw stuff'''
# open data file
rawFile = open('/Users/dsoto/current/swDataFlat/999-test-data/data/raw/test.data','r')
# read header, rip into dictionary
rawHeaderDict = getHeader(rawFile)
# grab data
# convert according to rx.cantilever and sign conventions
data = rx.readDataFileArray(rawFile)
# need to get cantilever values, micron conversion, and polarity stuff
cantileverDict = rx.getCantileverData(rawHeaderDict['cantilever'])
data = convertData(data,cantileverDict)

'''index stuff'''
# open index file
indexFile = open('/Users/dsoto/current/swDataFlat/999-test-data/traj/test.index','r')
# use matrix open from roxanne
# create dictionary from index entries
indexDict = rx.readDataFileArray(indexFile)
# converting string to float facilitates later formatting
indexDict['angle'] = map(float,indexDict['angle'])
#print dict to stdout
#print indexDict

# todo:check if file name exists (to deal with multiple trials)
for i in range(len(indexDict['angle'])):
    # construct file name
    fileOutName = '/Users/dsoto/current/swDataFlat/999-test-data/data/separated/pre-'
    fileOutName += 'a%02d.data' % indexDict['angle'][i]
    print fileOutName,
    print 'opening',
    fileOut = open(fileOutName,'w')
    print 'writing',
    outputDictAsText(rawHeaderDict, fileOut)
    outputDictAsTextByIndex(indexDict, i, fileOut)
    fileOut.write('<data>\n')
    # output header
    # output data list
    startIndex = int(indexDict['startIndex'][i])
    endIndex = int(indexDict['endIndex'][i])
    keys = data.keys()
    keys.sort()
    colWidth = max(map(len, keys)) + 1
    for key in keys:
        fileOut.write(key.ljust(colWidth))
    fileOut.write('\n')
    # get starting time
    startTime = data['time'][startIndex]
    for j in range(startIndex, endIndex + 1):
        for key in keys:
            if key == 'time':
                fileOut.write(str(data[key][j]-startTime).ljust(colWidth))
            else:
                fileOut.write(str(data[key][j]).ljust(colWidth))
        fileOut.write('\n')
    print 'finishing'
        #print '\n',



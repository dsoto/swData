#!/usr/bin/env python

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
import roxanne as rx
import numpy as np

fileNames = ['front','back']

for thisFileName in fileNames:
    fileName = thisFileName + '.data'

    fileIn = open(fileName, 'r')
    
    headDict = rx.readDataFileHeader(fileIn)
    dataDict = rx.readDataFileArray(fileIn)
    
    #print dataDict.keys()
    
    timeStrings = dataDict['time']
    timeSeconds = [float(ts[0:2])*3600+float(ts[3:5])*60+float(ts[6:]) 
                   for ts in timeStrings]
    
    import numpy as np
    timeSeconds = np.array(timeSeconds)
    timeSeconds = timeSeconds - timeSeconds[0]
    dataDict['time'] = map(str,timeSeconds)
    dataDict['time'] = timeSeconds
    
    voltageLateral        =  map(float,dataDict['voltageForceLateral'])
    voltageNormal         =  map(float,dataDict['voltageForceNormal'])
    voltageLateral        = -np.array(voltageLateral)
    voltageNormal         =  np.array(voltageNormal)

    mask = ((dataDict['time'] > 23) & (dataDict['time'] < 27))
    
    import matplotlib.pyplot as plt
    
    figure = plt.figure()
    axes = figure.add_subplot(111)
    axes.plot(dataDict['time'][mask], voltageNormal[mask],'b',
              label=thisFileName)
    axes.legend(loc='best')
    figure.savefig(thisFileName+'.pdf')

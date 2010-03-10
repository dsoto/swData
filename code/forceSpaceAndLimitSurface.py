#!/usr/bin/env python
'''
# plot all force space traces
# this script will plot all force space traces
# from a test sequence up to the point of failure


# read in analyzed.data file

# loop through file 
# open data files
# convert data to force
# plot data 
# color code data
'''
from __future__ import division
from __future__ import print_function
import sys
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
import roxanne as rx
import glob
import os.path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def convertToFloatArray(dataList):
    returnList = map(float, dataList)
    returnList = np.array(returnList)
    return returnList
  
def readDataFileArray(fileIn):

    tempLine = fileIn.readline()
    tempLine = tempLine.rstrip()
    headers = tempLine.split('\t')

    # TODO : strip whitespace from headers

    numColumns = len(headers)

    columnList = []
    for i in range(numColumns):
        columnList.append([])

    tempData = fileIn.readlines()

    # loop through data and append arrays
    for line in tempData:
        value = line.split('\t')
        for i in range(numColumns):
            columnList[i].append(value[i])

    columnDict = {}
    for i in range(numColumns):
        columnDict[headers[i]] = columnList[i]

    # tidy up and return values
    fileIn.close()
    return columnDict

def main():
    #dataDirectory = '../031-20100111-sws16-ls/data/separated/'
    dataDirectory = '../033-20100302-sws17-ls/data/separated/'
    parsedFileName = dataDirectory + '033-analyzedAngle.data'
    parsedFileName = dataDirectory + '033-parsed.dat'
    parseFileIn = open(parsedFileName)
    parseDict = rx.readDataFileArray(parseFileIn)
    angle = convertToFloatArray(parseDict['angle'])
    
    fileNameList = parseDict['dataFileName']
    
    

    for i,fileName in enumerate(fileNameList):
        fullFileName = dataDirectory + fileName
        print('processing file : ', fullFileName)
        
        fileIn = open(fullFileName)
        headerDict = rx.readDataFileHeader(fileIn)
        dataD = rx.readDataFileArray(fileIn)
        
        # convert lists to arrays of floats
        voltageLateral = convertToFloatArray(dataD['voltageForceLateral'])
        voltageNormal  = convertToFloatArray(dataD['voltageForceNormal'])
        positionNormalMicron = convertToFloatArray(dataD['voltagePositionX'])
        positionLateralMicron = convertToFloatArray(dataD['voltagePositionY'])
        
        # make conversions 
        voltageLateral = -voltageLateral
        voltageNormal = voltageNormal
        positionLateralMicron = positionLateralMicron * 10.0
        positionNormalMicron = positionNormalMicron * 10.0
        
        cantileverDict = rx.getCantileverData(headerDict['cantilever'])
        normalStiffness      = cantileverDict['normalStiffness']
        lateralStiffness     = cantileverDict['lateralStiffness']
        normalDisplacement   = cantileverDict['normalDisplacement']
        lateralDisplacement  = cantileverDict['lateralDisplacement']
        lateralAmplification = float(headerDict['latAmp'])
        normalAmplification  = float(headerDict['norAmp'])
        
        defaultAmplification = 100
        lateralDisplacement = (lateralDisplacement * lateralAmplification /
                                                     defaultAmplification)
        normalDisplacement = (normalDisplacement * normalAmplification /
                                                  defaultAmplification)
        
        # use cantilever values to convert voltages to forces
        lateralForceMuN = (voltageLateral *
                                   lateralStiffness / lateralDisplacement)
        normalForceMuN  = (voltageNormal * normalStiffness /
                                   normalDisplacement)
                                   
        # get location of filename in parseDict
        # and pull data from same index in the other arrays
        #fileName = os.path.splitext(fileName)
        #fileName = fileName[0]
        #fileNames = parseDict['dataFileName']
        #fileNameNoPath = os.path.split(fileName)[1]
        #indexFileName = fileNames.index(fileNameNoPath)

        # get indices for events in force trace
        indexContact     = parseDict['indexContact'][i]
        indexPreload     = parseDict['indexMaxPreload'][i]
        indexMaxAdhesion = parseDict['indexMaxAdhesion'][i]
        indexContact = int(indexContact)
        indexPreload = int(indexPreload)
        indexMaxAdhesion = int(indexMaxAdhesion)

        # get forces at contact, preload, pulloff
        normalForceContactMuN = normalForceMuN[indexContact]
        normalForcePreloadMuN = normalForceMuN[indexPreload]
        normalForcePulloffMuN = normalForceMuN[indexMaxAdhesion]

        shearForceContactMuN  = lateralForceMuN[indexContact]
        shearForcePreloadMuN  = lateralForceMuN[indexPreload]
        shearForcePulloffMuN  = lateralForceMuN[indexMaxAdhesion]

        #lateralForceMuN = lateralForceMuN[0:indexMaxAdhesion]
        #normalForceMuN = normalForceMuN[0:indexMaxAdhesion]
        
        # subtract off forces at contact?
        # slice forces [0:indexMaxAdhesion]

        lateralForceMuN -= shearForceContactMuN
        normalForceMuN -= normalForceContactMuN
        
        x = angle[i]/90.0
        myColor = (x,0,1-x)
        #print(myColor)
        
        plt.grid()
        plt.plot(lateralForceMuN, normalForceMuN, 
                 color = mpl.cm.get_cmap('jet')(x), 
                 label = str(i),
                 linewidth = 0.1,
                 alpha = 0.5)

        
        # plot forces on plot thang

    
    fileName = '033-analyzedAngle.data'
    fileIn = open(dataDirectory+fileName,'r')
    columnDict = readDataFileArray(fileIn)
    shearForce = map(float,columnDict['forceMaxShear'])
    normalForce = map(float,columnDict['forceMaxAdhesion'])
    preload = map(float,columnDict['preload'])
    angle = map(float,columnDict['angle'])
    
    shearForce = np.array(shearForce)
    normalForce = np.array(normalForce)
    preload = np.array(preload)
    preload = (preload - 29)*10
    angle = np.array(angle)
    

    
    plt.scatter(shearForce, 
                normalForce,
                marker = 'o',
                c=angle,
                s=preload,
                alpha=0.5)
    plt.xlabel('Shear Force (microNewtons)')
    plt.ylabel('Adhesion Force (microNewtons)')
    plt.title('Limit Surface sws17')
    plt.grid(True)
    colorbar = plt.colorbar()
    colorbar.set_label('angle of pulloff (90 is vertical)')
    #colorbar.set_label('preload distance')
    #plt.savefig('limitSurface.pdf',transparent=True)
    #plt.legend()
    #plt.colorbar()
    #plt.show()
    plt.savefig(dataDirectory+'forceSpace.pdf')
    return


if __name__ == '__main__':
    main()

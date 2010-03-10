#!/usr/bin/env python

# plotting script that expects a header line with labels for 
# each column of data
# these columns of data will be assigned to a dictionary
# returned values are all strings

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
import roxanne
import numpy as np

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
        line = line.rstrip()
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
    fileName = 'analyzed.data'
    fileIn = open(fileName,'r')
    columnDict = readDataFileArray(fileIn)
    shearForce  = map(float,columnDict['forceMaxShear'])
    normalForce = map(float,columnDict['forceMaxAdhesion'])
    preload     = map(float,columnDict['preload'])
    angle       = map(float,columnDict['angle'])
    
    shearForce  = np.array(shearForce)
    normalForce = np.array(normalForce)
    preload     = np.array(preload)
    angle       = np.array(angle)
    preload = (preload - 29)*10
    
    import matplotlib.pyplot as plt
    
    plt.scatter(shearForce, 
                normalForce,
                marker = 'o',
                c=angle,
                s=preload,
                alpha=0.5)
    plt.xlabel('Shear Force (microNewtons)')
    plt.ylabel('Adhesion Force (microNewtons)')
    plt.xlim((0,10.5))
    plt.ylim((-3.5,0))
    plt.title('sws10 - 529b02 - Limit Surface - 20090526')
    plt.grid(True)
    colorbar = plt.colorbar()
    colorbar.set_label('angle of pulloff (90 is vertical)')
    #colorbar.set_label('preload distance')
    plt.savefig('limitSurface.pdf',transparent=True)


if __name__ == '__main__':
    main()



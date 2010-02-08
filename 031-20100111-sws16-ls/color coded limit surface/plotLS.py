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
    # fileName = '../20091124-sws10-ls/data/separated/analyzed.data'
    # fileName = '../026-20091203-sws12-ls/data/separated/analyzed.data'
    fileName = '031-analyzed.data'
    fileIn = open(fileName,'r')
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
    
    import matplotlib.pyplot
    import matplotlib.axis
    import matplotlib
    
    
    matplotlib.pyplot.scatter(shearForce, 
                              normalForce,
                              marker = 'o',
                              c=angle,
                              s=preload,
                              alpha=0.5)
    matplotlib.pyplot.xlabel('Shear Force (microNewtons)')
    matplotlib.pyplot.ylabel('Adhesion Force (microNewtons)')
    matplotlib.pyplot.title('sws16 - 529b02 - Limit Surface - 20100111')
    matplotlib.pyplot.grid(True)
    colorbar = matplotlib.pyplot.colorbar()
    colorbar.set_label('angle of pulloff (90 is vertical)')
    #colorbar.set_label('preload distance')
    matplotlib.pyplot.savefig('limitSurface.pdf',transparent=True)


if __name__ == '__main__':
    main()



#!/usr/bin/env python

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
import roxanne as rx

parsedFileDirectory = '../027-20091203-sws13-ls/data/separated/'
parsedFileName = parsedFileDirectory + 'parsed.dat'
parsedFileObject = open(parsedFileName)

parsedDict = rx.readDataFileArray(parsedFileObject)

for i, fileName in enumerate(parsedDict['dataFileName']):
    indexContact    = int(parsedDict['indexContact'][i])
    indexMaxPreload = int(parsedDict['indexMaxPreload'][i])
    indexFailure    = int(parsedDict['indexMaxAdhesion'][i])
    fileName = parsedFileDirectory + fileName
    print fileName, indexContact
    rx.plotDataFileAnnotated(fileName, indexContact, 
                             indexMaxPreload, indexFailure)
    


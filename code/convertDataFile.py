#!/usr/bin/env python

# file to separate data file and convert to force and micron data
import roxanne as rx
import numpy as np
import os.path
import glob

directory = '../035-sws17-length/'
fileNameList = glob.glob(directory + 'data/raw/*.data')

for rawFileName in fileNameList:
    rawFile = open(rawFileName, 'r')
    #rawFile = open('~/current/swDataFlat/999-test-data/data/raw/test.data','r')

    # get full path name of input file
    fullRawFilePath = os.path.abspath(rawFileName)
    # separate path and filename
    tempPath, fileName = os.path.split(fullRawFilePath)
    tempPath = os.path.split(tempPath)[0]
    outPath = os.path.join(tempPath, 'separated')
    outFileName = os.path.join(outPath, fileName)

    '''output stuff'''
    print outFileName,
    print 'opening',
    fileOut = open(outFileName,'w')
    print 'writing',

    rx.convertDataFile(rawFile, fileOut)
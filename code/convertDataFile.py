#!/usr/bin/env python

# file to separate data file and convert to force and micron data
import roxanne as rx
import numpy as np


rawFile = open('/Users/dsoto/current/swDataFlat/999-test-data/data/raw/test.data','r')

'''output stuff'''
fileOutName = '/Users/dsoto/current/swDataFlat/999-test-data/data/separated/outFile.data'
print fileOutName,
print 'opening',
fileOut = open(fileOutName,'w')
print 'writing',

rx.convertDataFile(rawFile, fileOut)
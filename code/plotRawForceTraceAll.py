#!/usr/bin/env python

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
import roxanne
import glob

# fileNameList = glob.glob('../20091124-sws10-ls/data/separated/p3*.data')
# fileNameList = glob.glob('../20091124-sws11-ls/data/separated/p3*.data')
# fileNameList = glob.glob('../027-20091203-sws13-ls/data/separated/p3*.data')
fileNameList = glob.glob('../035-sws17-length/data/separated/*.data')

'''
fixme : put plots in /plot directory instead of data directory
'''

for fileName in fileNameList:
    roxanne.plotDataFileForce(fileName)
#!/usr/bin/env python

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
import roxanne
import glob

fileNameList = glob.glob('p3*.data')

for fileName in fileNameList:
#	roxanne.plotDataFileMPLPDF(fileName)
    roxanne.plotDataFileForce(fileName)
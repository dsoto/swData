#!/usr/bin/env python

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
import roxanne
import glob

fileNameList = glob.glob('*.data')

for fileName in fileNameList:
	roxanne.plotDataFileMPLPDF(fileName)

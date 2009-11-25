#!/usr/bin/env python

import sys
sys.path.append("../roxanne")
import roxanne
import glob

#fileNameList = glob.glob('data/p30/a*.0.data')
fileNameList = glob.glob('data/p35/a*.0.data')

for fileName in fileNameList:
#	roxanne.plotDataFileMPLPDF(fileName)
	roxanne.plotDataFileForce(fileName)



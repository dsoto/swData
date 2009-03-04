#!/usr/bin/env python

import sys
sys.path.append("../roxanne")
import roxanne
import glob

fileNameList = glob.glob('*.data')
for fileName in fileNameList:
	roxanne.plotDataFileMPLPDF(fileName)
#	roxanne.plotDataFileChacoPDF(fileName)
#	roxanne.plotDataFileChacoPNG(fileName)



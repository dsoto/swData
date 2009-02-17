#!/usr/bin/env python

import roxanne
import glob

fileNameList = glob.glob('*.data')
for fileName in fileNameList:
	
	roxanne.plotDataFileChaco(fileName)
	roxanne.plotDataFileChacoPNG(fileName)



#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

#---
def plotDataFile(fileName):
	import os.path
	import matplotlib.pyplot
	baseFileName = os.path.splitext(fileName)
	baseFileName = baseFileName[0]
	plotFileName = baseFileName + '.pdf'
	dataArray = readDataFile(fileName)
	time = dataArray[0]
	voltageNormal = dataArray[1]
	voltageShear = dataArray[2]
	positionX = dataArray[3]
	positionY = dataArray[4]
	
	matplotlib.pyplot.plot(voltageNormal)
	matplotlib.pyplot.hold(True)
	matplotlib.pyplot.plot(voltageShear)
	matplotlib.pyplot.hold(False)
	matplotlib.pyplot.xlabel('Time (ms)')
	matplotlib.pyplot.ylabel('Piezo Voltage Signal (V)')
	matplotlib.pyplot.savefig(plotFileName,transparent=True)
	return 0
	
#---
def readDataFile(fileName):
	# read in file
	fileIn = open(fileName,'r')
	tempData = fileIn.readlines()
	# initialize data arrays
	strings=[]
	column1=[]
	column2=[]
	column3=[]
	column4=[]
	# loop through data and append arrays
	for line in tempData:
		line=line.replace('\n','')
		value=line.split('\t')
		strings.append(value[0])
		column1.append(float(value[1]))
		column2.append(float(value[2]))
		column3.append(float(value[3]))
		column4.append(float(value[4]))
	# tidy up and return values
	fileIn.close()
	return [strings,column1,column2,column3,column4]
	

# ---- #
# MAIN #
# ---- #
	
import glob
fileNameList = glob.glob('*.data')
for fileName in fileNameList:
	plotDataFile(fileName)
	
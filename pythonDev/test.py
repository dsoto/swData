#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

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
	
# call function	
	
from pylab import *

fileName = 'data.data'
dataArray = readDataFile(fileName)
time = dataArray[0]
voltageNormal = dataArray[1]
voltageShear = dataArray[2]
positionX = dataArray[3]
positionY = dataArray[4]

plot(voltageNormal)
hold(True)
plot(voltageShear)
savefig('plot.pdf')
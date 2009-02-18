#!/usr/bin/env python

def addToDict(kvDict, key, tempLine):
	index = tempLine.find('=')+1
	length = len(tempLine)
	val = tempLine[index-length:]
	kvDict.update({key:val})			
	return kvDict			

def readDataFile(fileName):
	print 'readDataFile ' + fileName
	# read in file
	fileIn = open(fileName,'r')
	# read in lines until find data tag
	# if line contains '=' put entries in dictionary
	
	kvDict = {}
	keepReading = 1
	while keepReading == 1:
		tempLine = fileIn.readline()
		tempLine = tempLine.lower()
		tempLine = tempLine.rstrip()
		#print tempLine
		if tempLine.find('normal') != -1:
			key = 'norAmp'
			kvDict = addToDict(kvDict, key, tempLine)
# 			index = tempLine.find('=')+1
# 			length = len(tempLine)
# 			val = tempLine[index-length:]
# 			kvDict.update({key:val})			
		if tempLine.find('lateral') != -1:
			key = 'latAmp'
			kvDict = addToDict(kvDict, key, tempLine)
# 			index = tempLine.find('=')+1
# 			length = len(tempLine)
# 			val = tempLine[index-length:]
# 			kvDict.update({key:val})
		if tempLine.find('data starts here')!=-1:
			keepReading = 0
		
	fileIn.readline()
		
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
	return [strings,column1,column2,column3,column4,kvDict]

list=readDataFile('data/st_sws10_20090211_145840.data')
kvDict = list[5]
print kvDict
latAmp = kvDict['latAmp']
latAmp = float(latAmp)
print latAmp
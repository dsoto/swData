#!/usr/bin/env python

def addToDict(kvDict, key, tempLine):
	index = tempLine.find('=')+1
	length = len(tempLine)
	val = tempLine[index-length:]
	kvDict.update({key:val})			
	return kvDict			

def readDataFileHeader(fileIn):
	# read in file
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
		if tempLine.find('lateral') != -1:
			key = 'latAmp'
			kvDict = addToDict(kvDict, key, tempLine)
		if tempLine.find('roll') != -1:
			key = 'rollAngle'
			kvDict = addToDict(kvDict, key, tempLine)
		if tempLine.find('pitch') != -1:
			key = 'pitchAngle'
			kvDict = addToDict(kvDict, key, tempLine)

		if tempLine.find('data starts here')!=-1:
			keepReading = 0
		
	fileIn.readline()
	return [fileIn,kvDict]	
		
def readDataFileArray(fileIn):
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

def readIndexFile(fileName):
#	print 'readIndexFile ' + fileName
	fileIn = open(fileName,'r')
	# toss first three lines
	for i in range(3):
		tempLine = fileIn.readline()
	tempData = fileIn.readlines()
	# initialize data arrays
	fileNames = []
	indexContact = []
	indexPreload = []
	indexAdhesion = []
	# loop through data and append arrays
	for line in tempData:
		line=line.replace('\n','')
		value=line.split('\t')
		fileNames.append(value[0])
		indexContact.append(int(value[1]))
		indexPreload.append(int(value[2]))
		indexAdhesion.append(int(value[3]))
	# tidy up and return values
	fileIn.close()
	return [fileNames,indexContact,indexPreload,indexAdhesion]

def main():
	
	import glob
	import os.path
	import numpy
	
	indexList = readIndexFile('parsed.data')
	fOut = open('test.data','w')
	fileNameList = glob.glob('st_sws10_*.data')
	for fileName in fileNameList:
		fileIn = open(fileName)
		returnList = readDataFileHeader(fileIn)
		fileIn = returnList[0]
		kvDict = returnList[1]
		
		dataList = readDataFileArray(fileIn)

		lateralVoltage        = -numpy.array(dataList[1])
		normalVoltage         = numpy.array(dataList[2])
		positionNormalMicron  = dataList[3] * 10
		positionLateralMicron = dataList[4] * 10
						
		normalStiffness      = 0.313
		lateralStiffness     = 0.307
		normalDisplacement   = 0.148
		lateralDisplacement  = 0.437
		lateralAmplification = float(kvDict['latAmp'])
		normalAmplification  = float(kvDict['norAmp'])
		rollAngle            = float(kvDict['rollAngle'])
		pitchAngle           = float(kvDict['pitchAngle'])
		
		defaultAmplification = 100
		lateralDisplacement = (lateralDisplacement * lateralAmplification /
													 defaultAmplification)
		normalDisplacement = (normalDisplacement * normalAmplification /
 												 defaultAmplification)
 												 
		# use cantilever values to convert voltages to forces
		lateralForceMicroNewton = (lateralVoltage * 
		                           lateralStiffness / lateralDisplacement)
		normalForceMicroNewton  = (normalVoltage * normalStiffness /
		                           normalDisplacement)

#		print len(lateralForceMicroNewton)

		fileName = os.path.splitext(fileName)
		fileName = fileName[0]
		fileNames = indexList[0]
		indexFileName = fileNames.index(fileName)	

		indexContact     = indexList[1][indexFileName]
		indexPreload     = indexList[2][indexFileName]
		indexMaxAdhesion = indexList[3][indexFileName]

#		print indexContact
#		print indexMaxPreload
#		print indexMaxAdhesion

		# get forces at contact, preload, pulloff	
		normalForceContactMicroNewton = normalForceMicroNewton[indexContact]
		shearForceContactMicroNewton  = lateralForceMicroNewton[indexContact]
		normalForcePreloadMicroNewton = normalForceMicroNewton[indexPreload]
		shearForcePreloadMicroNewton  = lateralForceMicroNewton[indexPreload]
		normalForcePulloffMicroNewton = normalForceMicroNewton[indexMaxAdhesion]
		shearForcePulloffMicroNewton  = lateralForceMicroNewton[indexMaxAdhesion]

		normalCantileverVoltageMaxAdhesion = normalVoltage[indexMaxAdhesion]
		# get stage displacement at max adhesion
		normalStagePositionMaxAdhesion = positionNormalMicron[indexMaxAdhesion]
		# get cantilever deflection at contact
		normalCantileverVoltageContact = normalVoltage[indexContact]
		# get stage displacement at contact
		normalStagePositionContact = positionNormalMicron[indexContact]
		# calculate effective stage preload
		normalStagePreload = (normalStagePositionMaxAdhesion - 
													normalStagePositionContact)
		# calculate effective cantilever deflection
		normalCantileverDeflection = ((normalCantileverVoltageContact - 
                                   normalCantileverVoltageMaxAdhesion)/
                                   normalDisplacement)
		# calculate effective microwedge deflection (effective preload)
		effectivePreload = normalCantileverDeflection + normalStagePreload
		# adhesion force = maxAdhesion - force at contact
		maxAdhesionMicroNewton = (normalForcePulloffMicroNewton - 
															normalForceContactMicroNewton)
		# shear force = maxShear - force at contact
		maxShearMicroNewton = (shearForcePulloffMicroNewton - 
													 shearForceContactMicroNewton)

#		print indexContact
#		input()
		fOut.write(fileName + '\t')
		fOut.write('%5.1f\t' % pitchAngle )
		fOut.write('%5.3f\t' % effectivePreload)
		fOut.write('%5.3f\t' % maxAdhesionMicroNewton)
		fOut.write('%5.3f\t' % maxShearMicroNewton)
		fOut.write('\n')
	
	fOut.close()

if __name__ == '__main__':
	main()

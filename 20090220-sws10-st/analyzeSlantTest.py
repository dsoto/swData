#!/usr/bin/env python

# TODO : fix cantilever parameter fetching
#      : fix directory traversal problem


def addToDict(kvDict, key, tempLine):
	index = tempLine.find('=')+1
	length = len(tempLine)
	val = tempLine[index-length:]
	val = val.lstrip()
	kvDict.update({key:val})
	return kvDict

def getCantileverData(cantilever):
	cantileverDict = {}
	if cantilever == '529b02':
		lateralStiffness    = 3.898
		normalStiffness     = 0.659
		lateralDisplacement = 1.148
		normalDisplacement  = 0.224

	if cantilever == '629a03':
		lateralStiffness    = 0.307
		normalStiffness     = 0.313
		lateralDisplacement = 0.473
		normalDisplacement  = 0.148

	cantileverDict['lateralStiffness']    = lateralStiffness
	cantileverDict['normalStiffness']     = normalStiffness
	cantileverDict['lateralDisplacement'] = lateralDisplacement
	cantileverDict['normalDisplacement']  = normalDisplacement

	return cantileverDict

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
		if tempLine.find('cantilever') != -1:
			key = 'cantilever'
			kvDict = addToDict(kvDict, key, tempLine)

		if tempLine.find('<data>')!=-1:
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
	fOut = open('analyzed.data','w')
	fileNameList = glob.glob('sws10_st_*.data')
	for fileName in fileNameList:
		print 'processing file : ' + fileName
		fileIn = open(fileName)
		returnList = readDataFileHeader(fileIn)
		fileIn = returnList[0]
		kvDict = returnList[1]

		dataList = readDataFileArray(fileIn)

		lateralVoltage        = -numpy.array(dataList[1])
		normalVoltage         = numpy.array(dataList[2])
		positionNormalMicron  = numpy.array(dataList[3]) * 10
		positionLateralMicron = numpy.array(dataList[4]) * 10

		cantileverDict = getCantileverData(kvDict['cantilever'])

		normalStiffness      = cantileverDict['normalStiffness']
		lateralStiffness     = cantileverDict['lateralStiffness']
		normalDisplacement   = cantileverDict['normalDisplacement']
		lateralDisplacement  = cantileverDict['lateralDisplacement']
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
		normalForcePreloadMicroNewton = normalForceMicroNewton[indexPreload]
		normalForcePulloffMicroNewton = normalForceMicroNewton[indexMaxAdhesion]

		shearForceContactMicroNewton  = lateralForceMicroNewton[indexContact]
		shearForcePreloadMicroNewton  = lateralForceMicroNewton[indexPreload]
		shearForcePulloffMicroNewton  = lateralForceMicroNewton[indexMaxAdhesion]

		normalCantileverVoltageContact     = normalVoltage[indexContact]
		normalCantileverVoltagePreload     = normalVoltage[indexPreload]
		normalCantileverVoltageMaxAdhesion = normalVoltage[indexMaxAdhesion]

		normalStagePositionContact     = positionNormalMicron[indexContact]
		normalStagePositionPreload     = positionNormalMicron[indexPreload]
		normalStagePositionMaxAdhesion = positionNormalMicron[indexMaxAdhesion]

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
		# calculate effective stiffness of structure
		# force at preload - force at contact = force of preload
		forcePreload = normalForcePreloadMicroNewton - normalForceContactMicroNewton
		stageMovement = normalStagePositionPreload - normalStagePositionContact
		normalCantileverDeflection = ((normalCantileverVoltageContact -
                                   normalCantileverVoltagePreload)/
                                   normalDisplacement)

		# stage movement between contact and preload - cantilever deflection
		effectiveStiffness = forcePreload/(stageMovement-normalCantileverDeflection)

#		print indexContact
#		input()
		fOut.write(fileName + '\t')
		fOut.write('% 5.1f\t' % pitchAngle )
#		fOut.write('% 5.3f\t' % effectivePreload)
		fOut.write('% 5.3f\t' % maxAdhesionMicroNewton)
		fOut.write('% 5.3f\t' % maxShearMicroNewton)
#		fOut.write('% 5.3f\t' % normalStagePositionPreload)
#		fOut.write('% 5.3f\t' % normalStagePositionContact)
#		fOut.write('% 5.3f\t' % forcePreload)
#		fOut.write('% 5.3f\t' % stageMovement)
#		fOut.write('% 5.3f\t' % effectiveStiffness)
		fOut.write('\n')

	fOut.close()

if __name__ == '__main__':
	main()

#!/usr/bin/env python



def main():
	import sys
	sys.path.append('../../roxanne')
	import roxanne
	import glob
	import os.path
	import numpy

	parseFileIn = open('parsed.data','r')
	parseDict = roxanne.readDataFileArray(parseFileIn)
	print parseDict.keys()
	
	fOut = open('analyzed.data','w')
	fileNameList = glob.glob('sws10*.data')
	outputList = ['fileName',
	              'anglePitch',
	              'forceMaxAdhesion',
	              'forceMaxShear',
	              'anglePulloff']
	sep = '\t'
	headerString = sep.join(outputList)
	fOut.write(headerString)
	
	for fileName in fileNameList:

		print 'processing file : ' + fileName

		# TODO - pulloff angle from trajectory file name

		fileIn = open(fileName)
		headerDict = roxanne.readDataFileHeader(fileIn)
		dataDict = roxanne.readDataFileArray(fileIn)

		voltageLateral        =  map(float,dataDict['voltageForceLateral'])
		voltageNormal         =  map(float,dataDict['voltageForceNormal'])
		positionNormalMicron  =  map(float,dataDict['voltagePositionX']) * 10
		positionLateralMicron =  map(float,dataDict['voltagePositionY']) * 10

		voltageLateral        = -numpy.array(voltageLateral)
		voltageNormal         =  numpy.array(voltageNormal)
		positionNormalMicron  =  numpy.array(positionNormalMicron) * 10
		positionLateralMicron =  numpy.array(positionLateralMicron) * 10

		cantileverDict = roxanne.getCantileverData(headerDict['cantilever'])

		normalStiffness      = cantileverDict['normalStiffness']
		lateralStiffness     = cantileverDict['lateralStiffness']
		normalDisplacement   = cantileverDict['normalDisplacement']
		lateralDisplacement  = cantileverDict['lateralDisplacement']
		lateralAmplification = float(headerDict['latAmp'])
		normalAmplification  = float(headerDict['norAmp'])
		rollAngle            = float(headerDict['rollAngle'])
		pitchAngle           = float(headerDict['pitchAngle'])
#		anglePulloff         = float(headerDict['anglePulloff'])

		defaultAmplification = 100
		lateralDisplacement = (lateralDisplacement * lateralAmplification /
													 defaultAmplification)
		normalDisplacement = (normalDisplacement * normalAmplification /
 												 defaultAmplification)

		# use cantilever values to convert voltages to forces
		lateralForceMuN = (voltageLateral *
		                           lateralStiffness / lateralDisplacement)
		normalForceMuN  = (voltageNormal * normalStiffness /
		                           normalDisplacement)

		# get location of filename in parseDict
		# and pull data from same index in the other arrays
		fileName = os.path.splitext(fileName)
		fileName = fileName[0]
		fileNames = parseDict['dataFileName']
		indexFileName = fileNames.index(fileName)

		indexContact     = parseDict['indexContact'][indexFileName]
		indexPreload     = parseDict['indexMaxPreload'][indexFileName]
		indexMaxAdhesion = parseDict['indexMaxAdhesion'][indexFileName]
		
		indexContact = int(indexContact)
		indexPreload = int(indexPreload)
		indexMaxAdhesion = int(indexMaxAdhesion)

		# get forces at contact, preload, pulloff
		normalForceContactMuN = normalForceMuN[indexContact]
		normalForcePreloadMuN = normalForceMuN[indexPreload]
		normalForcePulloffMuN = normalForceMuN[indexMaxAdhesion]

		shearForceContactMuN  = lateralForceMuN[indexContact]
		shearForcePreloadMuN  = lateralForceMuN[indexPreload]
		shearForcePulloffMuN  = lateralForceMuN[indexMaxAdhesion]

		normalCantileverVoltageContact     = voltageNormal[indexContact]
		normalCantileverVoltagePreload     = voltageNormal[indexPreload]
		normalCantileverVoltageMaxAdhesion = voltageNormal[indexMaxAdhesion]

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
		maxAdhesionMuN = (normalForcePulloffMuN -
															normalForceContactMuN)
		# shear force = maxShear - force at contact
		maxShearMuN = (shearForcePulloffMuN -
													 shearForceContactMuN)
		# calculate effective stiffness of structure
		# force at preload - force at contact = force of preload
		forcePreload = normalForcePreloadMuN - normalForceContactMuN
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
		fOut.write('% 5.3f\t' % maxAdhesionMuN)
		fOut.write('% 5.3f\t' % maxShearMuN)
#		fOut.write('% 5.3f\t' % normalStagePositionPreload)
#		fOut.write('% 5.3f\t' % normalStagePositionContact)
#		fOut.write('% 5.3f\t' % forcePreload)
#		fOut.write('% 5.3f\t' % stageMovement)
#		fOut.write('% 5.3f\t' % effectiveStiffness)
		fOut.write('\n')

	fOut.close()

if __name__ == '__main__':
	main()

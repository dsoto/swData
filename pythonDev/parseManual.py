#!/usr/bin/env python
# parseManual.py
# python implementation of parse script to find points 

# load in headers using roxanne
# load in data using roxanne

# perform max/min analysis to find points
# store point in Array

import numpy   as np
import sys
sys.path.append("../roxanne")
import roxanne as rx

fileName = 'sws10-ls-155936.data'
fileIn = open(fileName,'r')
hD = rx.readDataFileHeader(fileIn)
dD = rx.readDataFileArray(fileIn)

print dD
print hD
	
# 	for fileName in fileNameList:
# 
# 		print 'processing file : ' + fileName
# 
# 		# TODO - pulloff angle from trajectory file name
# 
# 		fileIn = open(fileName)
# 		headerDict = roxanne.readDataFileHeader(fileIn)
# 		dataDict = roxanne.readDataFileArray(fileIn)
# 
# 		voltageLateral        =  map(float,dataDict['voltageForceLateral'])
# 		voltageNormal         =  map(float,dataDict['voltageForceNormal'])
# 		positionNormalMicron  =  map(float,dataDict['voltagePositionX']) * 10
# 		positionLateralMicron =  map(float,dataDict['voltagePositionY']) * 10
# 
# 		voltageLateral        = -numpy.array(voltageLateral)
# 		voltageNormal         =  numpy.array(voltageNormal)
# 		positionNormalMicron  =  numpy.array(positionNormalMicron) * 10
# 		positionLateralMicron =  numpy.array(positionLateralMicron) * 10
# 
# 		cantileverDict = roxanne.getCantileverData(headerDict['cantilever'])
# 
# 		normalStiffness      = cantileverDict['normalStiffness']
# 		lateralStiffness     = cantileverDict['lateralStiffness']
# 		normalDisplacement   = cantileverDict['normalDisplacement']
# 		lateralDisplacement  = cantileverDict['lateralDisplacement']
# 		lateralAmplification = float(headerDict['latAmp'])
# 		normalAmplification  = float(headerDict['norAmp'])
# 		rollAngle            = float(headerDict['rollAngle'])
# 		pitchAngle           = float(headerDict['pitchAngle'])
# #		anglePulloff         = float(headerDict['anglePulloff'])
# 
# 		defaultAmplification = 100
# 		lateralDisplacement = (lateralDisplacement * lateralAmplification /
# 													 defaultAmplification)
# 		normalDisplacement = (normalDisplacement * normalAmplification /
#  												 defaultAmplification)
# 
# 		# use cantilever values to convert voltages to forces
# 		lateralForceMuN = (voltageLateral *
# 		                           lateralStiffness / lateralDisplacement)
# 		normalForceMuN  = (voltageNormal * normalStiffness /
# 		                           normalDisplacement)
# 	% flags to perform analysis and plotting
# 	analyze = 1       % perform analysis of forces
# 	stdOutput = 0     % output to command line
# 	filterSpikes = 0  % filter sharp piezo spikes
# 	doDisplayPlot = 1  % display plot
# 	doPrintPlot = 1     % output a pdf plot 
# 	% doDisplayPlot doesn't work
# 	
# 	
# 	% need to extract only file name from trajectory file name
# 	% since the file string is on a PC this is all fucked 
# 	% search for PC path separator
# 	index = strfind(trajectoryFileName,'\')
# 	% get last one
# 	index = index(length(index))
# 	% rest of string is the actual filename
# 	trajectoryFileName = trajectoryFileName(index+1:length(trajectoryFileName))
# 	
# 	% get short filenames
# 	[pathstr, shortTrajectoryFileName, ext, ver] = fileparts(trajectoryFileName)
# 	[pathstr, shortDataFileName, ext, ver] = fileparts(dataFileName)
# 	
# 	
# 	
# 	% assemble plot file name and title from the tokens above
# 	plotFileName = sprintf('./plots/%s_p%s_pa%s_ra%s_ls', ...
# 												 sample,preload,pitchAngle,rollAngle)
# 	titleString = sprintf('%s preload %s pitch angle %s roll angle %s ls',... 
# 												 sample,preload,pitchAngle,rollAngle)
# 	
# 	
# 	cantilever = cantilever(14:19)
# 	% call function to get cantilever parameters
# 	[normalStiffness, lateralStiffness, ...
# 	 normalDisplacement, lateralDisplacement] = ...
# 	 getCantileverData(cantilever)
# 	
# 	% now displacement is corrected for gain setting on box 
# 	defaultAmplification = 100
# 	lateralDisplacement = lateralDisplacement * lateralAmplification / ...
# 												defaultAmplification
# 	normalDisplacement = normalDisplacement * normalAmplification / ...
# 											 defaultAmplification
# 	
# 	% load data from file into array
# 	dataArray = textscan(fileHandle, '%s %15.7f %15.7f %15.7f %15.7f')
# 	fclose(fileHandle)
# 	
# 	lateralVoltage         = -dataArray{1,2}
# 	normalVoltage          =  dataArray{1,3}
# 	positionNormalMicron   =  dataArray{1,4} * 10
# 	positionLateralMicron  =  dataArray{1,5} * 10
# 	
# 	if debug
# 	lateralVoltage(1)
# 	end
# 	
# 	% pull out relevant data section
# 	% as written this is redundant but 
# 	% this section can be adjusted easily to look at 
# 	% a subset of the data
# 	dataStart = 1
# 	dataEnd = length(lateralVoltage)
# 	lateralVoltage = lateralVoltage(dataStart:dataEnd) %???
# 	normalVoltage = normalVoltage(dataStart:dataEnd) %???
# 	
# 	% filter spikes
# 	if (filterSpikes == 1)
# 		spikeFactor = 3
# 		lateralVoltage = filterSpikes(lateralVoltage, spikeFactor)
# 		normalVoltage = filterSpikes(normalVoltage, spikeFactor)
# 	end
# 	
# 	% use cantilever values to convert voltages to forces
# 	lateralForceMicroNewton = ... 
# 		lateralVoltage * lateralStiffness / lateralDisplacement
# 	normalForceMicroNewton = ... 
# 		normalVoltage * normalStiffness / normalDisplacement
# 	
# 	%
# 	% automated point detection 
# 	
# 	% find maximum (negative) adhesion value this is pulloff
# 	[maxAdhesionUncompensatedMicroNewton,indexMaxAdhesion] = ...
# 		min(normalForceMicroNewton)
# 	% store shear value corresponding to max adhesion
# 	maxShearUncompensatedMicroNewton = lateralForceMicroNewton(indexMaxAdhesion)
# 	% back up and find maximum normal value this is max preload
# 	[maxPreloadMicroNewton,indexMaxPreload] = ...
# 		max(normalForceMicroNewton(1:indexMaxAdhesion))
# 	% back up and find min normal value this is point of contact
# 	[normalForceContactMicroNewton, indexContact] = ...
# 		min(normalForceMicroNewton(1:indexMaxPreload))
# 	% find corresponding value of contact for shear
# 	shearForceContactMicroNewton = lateralForceMicroNewton(indexContact)
# 	
# 	%
# 	% automated plot presentation
# 	
# 	% plot normal and shear traces 
# 	plot(lateralForceMicroNewton,'g')
# 	hold on
# 	plot(normalForceMicroNewton,'b')
# 	
# 	% plot maximum adhesion point
# 	plot(indexMaxAdhesion, maxAdhesionUncompensatedMicroNewton,'bo')
# 	
# 	% plot corresponding max shear point
# 	plot(indexMaxAdhesion, maxShearUncompensatedMicroNewton,'go')
# 	
# 	% plot maximum preload point
# 	plot(indexMaxPreload, maxPreloadMicroNewton,'ro')
# 	
# 	% plot normal contact position
# 	plot(indexContact, normalForceContactMicroNewton,'bd')
# 	
# 	% plot shear contact position
# 	plot(indexContact, shearForceContactMicroNewton,'gd')
# 	hold off
# 	
# 	xlabel('Time (ms)')
# 	ylabel('Force (microNewtons)')
# 	legend('Shear','Normal','Max Normal Adhesion', ...
# 				 'Max Shear Adhesion', 'Max Preload', ...
# 				 'Normal Contact Point', 'Shear Contact Point')		
# 	title({titleString},'Interpreter','None')
# 	
# 	%
# 	% check if automated detection was acceptable
# 	
# 	fprintf(1,'Are these points acceptable? (y/n) \n')
# 	response = input(' : ','s')
# 	isAcceptable = strcmp('y',response)
# 	
# 	if (isAcceptable == 1)
# 		fprintf(1,'You accepted\n')
# 	end
# 	
# 		
# 
# 	% output to log file
# 	fprintf(logFileHandle, '% 20s\t',   shortDataFileName)
# 	fprintf(logFileHandle, '% 15d\t', indexContact)
# 	fprintf(logFileHandle, '% 15d\t', indexMaxPreload)
# 	fprintf(logFileHandle, '% 15d',   indexMaxAdhesion)
# 	fprintf(logFileHandle, '\n')
# 		

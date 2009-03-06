#!/usr/bin/env python
# parseManual.py
# python implementation of parse script to find points 

# load in headers using roxanne
# load in data using roxanne

# perform max/min analysis to find points
# store point in Array

import matplotlib.pyplot as mpl
import numpy      as np
import sys
sys.path.append("../roxanne")
import roxanne    as rx

fileName = 'sws10-ls-155936.data'
fileIn = open(fileName,'r')
# header dictionary
hD = rx.readDataFileHeader(fileIn)
# data dictionary
dD = rx.readDataFileArray(fileIn)

print hD
	
voltageLateral        =  map(float,dD['voltageForceLateral'])
voltageNormal         =  map(float,dD['voltageForceNormal'])
positionNormalMicron  =  map(float,dD['voltagePositionX']) * 10
positionLateralMicron =  map(float,dD['voltagePositionY']) * 10

voltageLateral        = -np.array(voltageLateral)
voltageNormal         =  np.array(voltageNormal)
positionNormalMicron  =  np.array(positionNormalMicron) * 10
positionLateralMicron =  np.array(positionLateralMicron) * 10

# cantilever dictionary
cD = rx.getCantileverData(hD['cantilever'])
 
normalStiffness      = cD['normalStiffness']
lateralStiffness     = cD['lateralStiffness']
normalDisplacement   = cD['normalDisplacement']
lateralDisplacement  = cD['lateralDisplacement']
lateralAmplification = float(hD['latAmp'])
normalAmplification  = float(hD['norAmp'])
rollAngle            = float(hD['rollAngle'])
pitchAngle           = float(hD['pitchAngle'])
#anglePulloff         = float(hD['anglePulloff'])
# how do i get parameters from filename

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

mpl.plot(lateralForceMuN,'g')
mpl.plot(normalForceMuN,'b')
mpl.show()

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
# 	lateralForceMuN = ... 
# 		lateralVoltage * lateralStiffness / lateralDisplacement
# 	normalForceMuN = ... 
# 		normalVoltage * normalStiffness / normalDisplacement
# 	
# 	%
# 	% automated point detection 
# 	
# 	% find maximum (negative) adhesion value this is pulloff
# 	[maxAdhesionUncompensatedMuN,indexMaxAdhesion] = ...
# 		min(normalForceMuN)
# 	% store shear value corresponding to max adhesion
# 	maxShearUncompensatedMuN = lateralForceMuN(indexMaxAdhesion)
# 	% back up and find maximum normal value this is max preload
# 	[maxPreloadMuN,indexMaxPreload] = ...
# 		max(normalForceMuN(1:indexMaxAdhesion))
# 	% back up and find min normal value this is point of contact
# 	[normalForceContactMuN, indexContact] = ...
# 		min(normalForceMuN(1:indexMaxPreload))
# 	% find corresponding value of contact for shear
# 	shearForceContactMuN = lateralForceMuN(indexContact)
# 	
# 	%
# 	% automated plot presentation
# 	
# 	% plot normal and shear traces 
# 	plot(lateralForceMuN,'g')
# 	hold on
# 	plot(normalForceMuN,'b')
# 	
# 	% plot maximum adhesion point
# 	plot(indexMaxAdhesion, maxAdhesionUncompensatedMuN,'bo')
# 	
# 	% plot corresponding max shear point
# 	plot(indexMaxAdhesion, maxShearUncompensatedMuN,'go')
# 	
# 	% plot maximum preload point
# 	plot(indexMaxPreload, maxPreloadMuN,'ro')
# 	
# 	% plot normal contact position
# 	plot(indexContact, normalForceContactMuN,'bd')
# 	
# 	% plot shear contact position
# 	plot(indexContact, shearForceContactMuN,'gd')
# 	hold off
# 	
# 	xlabel('Time (ms)')
# 	ylabel('Force (MuNs)')
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

#!/usr/bin/env python

def main():	
	print 'roxanne.py'
	return 0

def generateTrajectory():
	print 'generateTrajectory'
	# function outputvector = generateTrajectory(verticesMicron,velocityMicronPerSecond,pathFileName);
	# 
	# % code to generate points for piezo movement
	# 
	# % verticesMicron = M by 2 list of vertices
	# % velocityMicronPerSecond = M-1 by 1 list of velocities
	# % pathFileName = file name under which points are saved
	# 
	# 
	# % adds quiet period of zeros to start and end of trajectory data
	# addTails = true;
	# timeTareMSec = 100;
	# timeSettleMSec = 100;
	# 
	# outdt = 1;   %time between output data points in milliseconds
	# acqdt = 1;    %time between acquired data points in milliseconds
	# 
	# numlegs = length(velocityMicronPerSecond);
	# 
	# path = [];
	# % put in initial series of zeros
	# numSteps = timeTareMSec / outdt;
	# tpath = zeros( numSteps, 2 );
	# path = [path; tpath];
	# 
	# path = [path; verticesMicron(1,:)];    %adds starting point to the path
	# for i = 1:numlegs  % loop through coordinates vector    
	#     d = sqrt( (verticesMicron(i+1,1) - verticesMicron(i,1))^2 + ...
	#               (verticesMicron(i+1,2) - verticesMicron(i,2))^2 );
	#     legtime = ( d/velocityMicronPerSecond(i) ) * 1000; %time in ms
	#     numsteps = ceil ( legtime / outdt );
	#     tpath = [ [1:numsteps]' [1:numsteps]' ];
	#     stepdist = (verticesMicron(i+1,:) - verticesMicron(i,:)) ./ numsteps;
	#     tpath(:,1) = stepdist(1) .* tpath(:,1) + verticesMicron(i,1);
	#     tpath(:,2) = stepdist(2) .* tpath(:,2) + verticesMicron(i,2);
	#     path = [path;tpath];
	# end
	# 
	# % put in trailing series of zeros
	# numSteps = timeSettleMSec / outdt;
	# tpath = zeros( numSteps, 2 );
	# path = [path; tpath];
	# 
	# 
	# % output file
	# outputvector = [ outdt acqdt; path ];
	# filename = [ pathFileName '.traj' ];
	# fid = fopen(filename, 'wt');
	# fprintf(fid, '%-6.2f\t%-6.2f\n', outputvector');
	# fclose(fid);
	# 
	# % show plot of trajectory
	# figure(1);
	# lov = size(outputvector,1);
	# plot(outputvector(2:lov,1),outputvector(2:lov,2),'b.');
	# title(pathFileName,'Interpreter','None');
	# xlabel('x-axis (micron)');
	# ylabel('y-axis (micron)');
	# axis([-10 100 -10 100]);
	# set(gca,'XDir','reverse');
	# set(gca,'YDir','reverse');
	# shg;
	print 'done'

def plotDataFileChacoPDF(fileName):
	import os.path
	import numpy

	baseFileName = os.path.splitext(fileName)
	baseFileName = baseFileName[0]
	plotFileName = baseFileName + 'Chaco.pdf'
	dataArray = readDataFile(fileName)
	time = dataArray[0]
	voltageNormal = dataArray[1]
	voltageShear = dataArray[2]
	positionX = dataArray[3]
	positionY = dataArray[4]	
	x = numpy.arange(len(voltageNormal))

	from enthought.chaco.api import ArrayPlotData, Plot, PlotGraphicsContext
	from enthought.chaco.pdf_graphics_context import PdfPlotGraphicsContext
	
	pd=ArrayPlotData(index=x)
	p = Plot(pd)
	pd.set_data("normal",voltageNormal)
	pd.set_data("shear",voltageShear)
	p.plot(("index","normal"),color='blue',width=2.0)
	p.plot(("index","shear"),color='green',width=2.0)
	p.padding = 50
	p.title = baseFileName
	p.x_axis.title = "Sample"
	p.y_axis.title = "Voltage (V)"
	p.bounds = ([800,600])
	p.do_layout(force=True)
	gcpdf = PdfPlotGraphicsContext(filename=plotFileName, 
	                            dest_box=(0.5,0.5,5.0,5.0))
	gcpdf.render_component(p)
	gcpdf.save()

def plotDataFileChacoPNG(fileName):
	import os.path
	import numpy

	baseFileName = os.path.splitext(fileName)
	baseFileName = baseFileName[0]
	plotFileName = baseFileName + 'Chaco.png'
	dataArray = readDataFile(fileName)
	time = dataArray[0]
	voltageNormal = dataArray[1]
	voltageShear = dataArray[2]
	positionX = dataArray[3]
	positionY = dataArray[4]	
	x = numpy.arange(len(voltageNormal))

	from enthought.traits.api import false
	from enthought.chaco.api import ArrayPlotData, Plot, PlotGraphicsContext
	from enthought.chaco.pdf_graphics_context import PdfPlotGraphicsContext
	
	pd=ArrayPlotData(index=x)
	p = Plot(pd,bgcolor="white",padding=50,border_visible=True)
	pd.set_data("normal",voltageNormal)
	pd.set_data("shear",voltageShear)
	p.plot(("index","normal"),color='blue',width=2.0)
	p.plot(("index","shear"),color='green',width=2.0)
	p.padding = 50
	p.title = baseFileName
	p.x_axis.title = "Sample"
	p.y_axis.title = "Voltage (V)"
	p.outer_bounds = ([800,600])
	p.do_layout(force=True)
	gcpng = PlotGraphicsContext(([800,600]),dpi=72)
	gcpng.render_component(p)
	gcpng.save(plotFileName)

def plotDataFileMPLPDF(fileName):
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
	matplotlib.pyplot.title(plotFileName)
	matplotlib.pyplot.savefig(plotFileName,transparent=True)
	matplotlib.pyplot.close()
	return 0

def getContactPoint(fileName):
	import os.path
#	import matplotlib.pyplot
	import pylab
	
	baseFileName = os.path.splitext(fileName)
	baseFileName = baseFileName[0]
	plotFileName = baseFileName + '.pdf'
	dataArray = readDataFile(fileName)
	time = dataArray[0]
	voltageNormal = dataArray[1]
	voltageShear = dataArray[2]
	positionX = dataArray[3]
	positionY = dataArray[4]
	
	pylab.figure(1)
	pylab.plot(voltageNormal)
#	pylab.hold(True)
	pylab.plot(voltageShear)
	pylab.xlabel('Time (ms)')
	pylab.ylabel('Piezo Voltage Signal (V)')
	pylab.title(plotFileName)
	points = pylab.ginput(2)
	points = pylab.array(points)
#	points = points[0]
	print points
	pylab.plot(points[:,0],points[:,1],'bo')
	# why won't this plot now???
	pylab.figure(1)
#	pylab.scatter(points,s=1,c='b',marker='o')
	pylab.waitforbuttonpress()
	pylab.savefig(plotFileName,transparent=True)
	pylab.close(1)
	return 0

def readDataFile(fileName):
	# read in file
	fileIn = open(fileName,'r')
	# read and discard first 9 lines of file
	for i in range(9):
		tempLine=fileIn.readline()
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

	return kvDict

def readDataFileArrayOld(fileIn):
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

def readDataFileArray(fileIn):
	
	tempLine = fileIn.readline()
	tempLine = tempLine.rstrip()
	headers = tempLine.split('\t')

	# TODO : strip whitespace from headers
	
	numColumns = len(headers)
	
	columnList = []
	for i in range(numColumns):
		columnList.append([])
	
	tempData = fileIn.readlines()

	# loop through data and append arrays
	for line in tempData:
		line=line.replace('\n','')
		value=line.split('\t')
		for i in range(numColumns):
			columnList[i].append(value[i])

	columnDict = {}
	for i in range(numColumns):
		columnDict[headers[i]] = columnList[i]
	
	# tidy up and return values
	fileIn.close()
	return columnDict

def parseForceTrace(hD,dD):

	import matplotlib.pyplot as mpl
	import numpy      as np
	import sys
	
	voltageLateral        =  map(float,dD['voltageForceLateral'])
	voltageNormal         =  map(float,dD['voltageForceNormal'])
	positionNormalMicron  =  map(float,dD['voltagePositionX']) * 10
	positionLateralMicron =  map(float,dD['voltagePositionY']) * 10
	
	voltageLateral        = -np.array(voltageLateral)
	voltageNormal         =  np.array(voltageNormal)
	positionNormalMicron  =  np.array(positionNormalMicron) * 10
	positionLateralMicron =  np.array(positionLateralMicron) * 10
	
	# cantilever dictionary
	cD = getCantileverData(hD['cantilever'])
	 
	normalStiffness      = cD['normalStiffness']
	lateralStiffness     = cD['lateralStiffness']
	normalDisplacement   = cD['normalDisplacement']
	lateralDisplacement  = cD['lateralDisplacement']
	
	# filter spikes

	normalForceZip = zip(voltageNormal,
											 np.arange(len(voltageNormal)))
	indexMaxAdhesion = min(normalForceZip)[1]
	normalForceZip = zip(voltageNormal[0:indexMaxAdhesion],
											 np.arange(indexMaxAdhesion))
	indexMaxPreload = max(normalForceZip)[1]
	normalForceZip = zip(voltageNormal[0:indexMaxPreload],
											 np.arange(indexMaxPreload))
	indexContact = min(normalForceZip)[1]
	
	index = {'indexContact'     : indexContact,
	         'indexMaxPreload'  : indexMaxPreload,
	         'indexMaxAdhesion' : indexMaxAdhesion}
	return index
	
if __name__ == '__main__':
	main()

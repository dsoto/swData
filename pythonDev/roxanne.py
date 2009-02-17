#!/usr/bin/env python

def main():	
	print 'roxanne.py'
	return 0

def generateTrajectory()
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

def plotDataFileChaco(fileName):
	import os.path
	import numpy

	baseFileName = os.path.splitext(fileName)
	baseFileName = baseFileName[0]
	plotFileName = baseFileName + '.pdf'
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
	plotFileName = baseFileName + '.png'
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
	matplotlib.pyplot.title(plotFileName)
	matplotlib.pyplot.savefig(plotFileName,transparent=True)
	matplotlib.pyplot.close()
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
		
if __name__ == '__main__':
	main()
	
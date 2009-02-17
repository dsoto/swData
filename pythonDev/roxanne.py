#!/usr/bin/env python

def main():	
	print 'roxanne.py'
	return 0

def plotDataFileChaco(fileName):
	import os.path
	import matplotlib.pyplot
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

	from enthought.chaco.api import ArrayPlotData,Plot
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
	gc = PdfPlotGraphicsContext(filename=plotFileName, 
	                            dest_box=(0.5,0.5,5.0,5.0))
	gc.render_component(p)
	gc.save()

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
	
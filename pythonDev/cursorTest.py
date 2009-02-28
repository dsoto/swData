#!/usr/bin/env python

import numpy
from enthought.chaco.api import create_line_plot, OverlayPlotContainer, \
                                HPlotContainer, Plot, ArrayPlotData
from enthought.enable.component_editor import ComponentEditor
from enthought.chaco.tools.cursor_tool import CursorTool, BaseCursorTool
from enthought.traits.api import HasTraits, Instance, Array
from enthought.traits.ui.api import View, Item
import glob
import sys
sys.path.append("../roxanne")
import roxanne


class plotBox(HasTraits):
	index = Array
	value = Array
	cursor = Instance(BaseCursorTool)
	hPlot = Instance(HPlotContainer)
	
	def __init__(self, fileName):
		super(plotBox, self).__init__()
		
		self.hPlot = HPlotContainer(padding = 50)
		leftPlot = OverlayPlotContainer(padding = 50)
		self.hPlot.add(leftPlot)
		rightPlot = OverlayPlotContainer(padding = 50)
		self.hPlot.add(rightPlot)
		
		self.fileName = fileName
		self.plotTitle = fileName
		
		fileIn = open(fileName,'r')
		roxanne.readDataFileHeader(fileIn)
		columnDict = roxanne.readDataFileArray(fileIn)
		
		self.value = numpy.array(map(float,columnDict['voltageForceNormal']))
		self.value2 = numpy.array(map(float,columnDict['voltageForceLateral']))
		self.index = numpy.arange(len(self.value))
		
		line = create_line_plot([self.index,self.value], add_grid=True, 
														add_axis=True, 
														color = 'blue',
														index_sort='ascending',
														orientation = 'h')
												
		line2 = create_line_plot([self.index,self.value2], add_grid=True, 
														add_axis=True, index_sort='ascending',
														orientation = 'h')
														
		self.cursor = CursorTool(line,color='blue')
		line.overlays.append(self.cursor)

		leftPlot.add(line)
		rightPlot.add(line2)
		self.hPlot.title = 'asoentuh'
			
	traits_view = View(Item('hPlot',
										      editor=ComponentEditor(),
										      resizable=True,
										      show_label=False),
                     title="Demo",
                     resizable=True,
                     width=800,height=400)
    

if __name__=='__main__':

	fileNameList = glob.glob('*.data')
	for fileName in fileNameList:
		myPlotBox = plotBox(fileName)
		myPlotBox.configure_traits()

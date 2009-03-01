#!/usr/bin/env python

import numpy
from enthought.chaco.api import create_line_plot, OverlayPlotContainer, \
                                VPlotContainer, Plot, ArrayPlotData
from enthought.enable.component_editor import ComponentEditor
from enthought.chaco.tools.cursor_tool import CursorTool, BaseCursorTool
from enthought.chaco.tools.api import ZoomTool, PanTool
from enthought.traits.api import HasTraits, Instance, Array, Button, Str
from enthought.traits.ui.menu import Action
from enthought.traits.ui.api import View, Item, Handler
import glob
import sys
sys.path.append("../roxanne")
import roxanne

class plotBoxHandler(Handler):

	def accept(self, info):
		info.object.message = 'plot points accepted'
		close(info)
		
	def reject(self, info):
		info.object.message = 'plot points rejected, choose again'
		

class plotBox(HasTraits):
	index = Array
	value = Array
	message = Str
	accept = Action(name = "Accept", action = "accept")
	reject = Action(name = "Reject", action = "reject")
	cursor = Instance(BaseCursorTool)
	hPlot = Instance(VPlotContainer)
	
	def __init__(self, fileName):
		super(plotBox, self).__init__()
		print fileName
		
		self.message = 'you like?'
		self.hPlot = VPlotContainer(padding = 10)
		leftPlot = OverlayPlotContainer(padding = 10)
		self.hPlot.add(leftPlot)
		rightPlot = OverlayPlotContainer(padding = 10)
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
														
		self.cursor = CursorTool(line,drag_button = 'left',color='blue')
		self.cursor.current_position = 1000,self.value[1000]
		line.overlays.append(self.cursor)
		line2.tools.append(ZoomTool(line2))

		leftPlot.add(line)
		rightPlot.add(line2)
		self.hPlot.title = 'asoentuh'

		
	traits_view = View(Item('hPlot',
										      editor = ComponentEditor(),
										      resizable = True,
										      show_label = False),
										 Item('message'),
										 buttons = [accept,reject],
                     title = 'Cursor Demo Test',
                     handler = plotBoxHandler(),
                     resizable = True,
                     width = 1400, height = 800,
                     x = 20, y = 40)

		
def main():
	fileNameList = glob.glob('*.data')
	for fileName in fileNameList:
		myPlotBox = plotBox(fileName)
		myPlotBox.configure_traits()


if __name__=='__main__':
	main()
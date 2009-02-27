#!/usr/bin/env python



from enthought.traits.api import (String, HasTraits, Button, Instance,
                                  Array)
from enthought.traits.ui.api import View, Item
from enthought.traits.ui.menu import OKButton, CancelButton
from enthought.chaco.api import Plot, ArrayPlotData
from enthought.enable.component_editor import ComponentEditor
import numpy
import glob
import os.path

class plotBox(HasTraits):
	x = Array
	y = Array
	plotAttribute = Instance(Plot)

	traits_view = View(
	              Item('plotAttribute',
	                   editor = ComponentEditor(),
	                   show_label = False),
                resizable = True,
	              height = 500,
                width = 500,
                title = 'Can Only Hard Code',
                x = 0.1,
                y = 0.1,
	              buttons = [OKButton, CancelButton])
	
 	def __init__(self, fileName):
		self.fileName = fileName
		self.plotTitle = fileName
		self.x = numpy.arange(-10,10,0.01)
		self.y = numpy.sin(self.x)
		
		self.plotdata = ArrayPlotData(x=self.x,y=self.y)
		self.plotAttribute = Plot(self.plotdata)
		self.plotAttribute.plot(("x","y"),type="line",color="blue",name='amp')
		self.plotAttribute.title = self.plotTitle

	
if __name__ == '__main__':

	fileNameList = glob.glob('*.data')
	for fileName in fileNameList:
		myPlotBox = plotBox(fileName)
		myPlotBox.configure_traits()

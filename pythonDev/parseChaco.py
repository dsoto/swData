#!/usr/bin/env python

from enthought.chaco.api               import (create_line_plot,
                                               OverlayPlotContainer,
                                               VPlotContainer, Plot, ArrayPlotData)
from enthought.chaco.tools.api         import (ZoomTool, PanTool, LineInspector,                
                                               DragZoom)
from enthought.traits.api              import (HasTraits, Instance, Array,
                                               Button, Str, Int, Float, Bool, DelegatesTo, Property, Disallow, cached_property, Tuple)
from enthought.traits.ui.api           import View, Item, Handler, HGroup
from enthought.traits.ui.menu          import Action, OKButton

from enthought.enable.component_editor import ComponentEditor

import numpy
import glob
import sys
sys.path.append("../roxanne")
import roxanne


class customTool(LineInspector):
	pointsClicked = Int
	
 	def __init__(self,*args,**kwargs):
 		super(customTool,self).__init__(*args,**kwargs)
 		self.plotBox = kwargs['plotBox']

	def normal_mouse_move(self, event):
		LineInspector.normal_mouse_move(self,event)
		plot = self.component
		plot.request_redraw()
		cursorPosX = self.component.map_data([event.x,event.y])[0]
		self.plotBox.cursorPosX = int(cursorPosX)
		self.plotBox.cursorPosY = self.plotBox.value[self.plotBox.cursorPosX]
		
	def normal_left_down(self, event):
		cursorPosX = self.component.map_data([event.x,event.y])[0]
		self.plotBox.cursorPosX = int(cursorPosX)
		self.plotBox.cursorPosY = self.plotBox.value[self.plotBox.cursorPosX]
		if self.pointsClicked < 3:
			#print self.pointsClicked,self.plotBox.cursorPosX, self.plotBox.cursorPosY
			self.plotBox.pointX[self.pointsClicked]=self.plotBox.cursorPosX
			self.plotBox.pointY[self.pointsClicked]=self.plotBox.cursorPosY
			print self.plotBox.pointX, self.plotBox.pointY
			self.plotBox.plotdata.set_data('pointX',self.plotBox.pointX)
			self.plotBox.plotdata.set_data('pointY',self.plotBox.pointY)
			self.pointsClicked += 1
			
	def normal_left_up(self, event):
		pass


class plotBoxHandler(Handler):

	def close(self, info, is_ok):
		if info.object.isAccepted == True:
			return True
	
	def closed(self, info, is_ok):
		pass
		#print 'window closed successfully'

	def accept(self, info):
		info.object.message = 'plot points accepted'
		info.object.isAccepted = True
		print info.object.pointX
		
	def reject(self, info):
		info.object.message = 'plot points rejected, choose again'
		info.object.isAccepted = False
	
	def object_pointX_changed(self,info):
		print info.object.pointX
		pass
		
class plotBox(HasTraits):
	index = Array
	value = Array
	value2 = Array
	pointX = Array(dtype=float,value=([0.0,100.0,200.0]))
#	pointX = numpy.array([0.0,0.0,0.0],dtype = float)
	pointY = Array(dtype=float,value=([0.0,0.0,0.0]))
#	pointY = numpy.array([0.0,0.0,0.0],dtype = float)
	message = Str
	isAccepted = Bool
	accept = Action(name = "Accept", action = "accept")
	reject = Action(name = "Reject", action = "reject")
	cursorPosX = Int
	cursorPosY = Float
	hPlot = Instance(VPlotContainer)
	
	def __init__(self, fileName):
		super(plotBox, self).__init__()

		self.message = 'Analysis Acceptable?'
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
		self.plotdata = ArrayPlotData(index = self.index,
		                              value = self.value,
		                              value2 = self.value2,
		                              pointX = self.pointX,
		                              pointY = self.pointY)
		self.shearPlot = Plot(self.plotdata)
		self.shearPlot.plot(('index','value'),type='line',color='blue')
		self.shearPlot.plot(('pointX','pointY'),type='scatter',color='red')
		self.normalPlot = Plot(self.plotdata)
		self.normalPlot.plot(('index','value2'),type='line',color='green')
														
		self.shearPlot.overlays.append(customTool(plotBox = self,
		                                   component=self.shearPlot,
		                                   axis = 'index_x',
		                                   inspect_mode='indexed',
		                                   write_metadata=True,
		                                   color='black',
		                                   is_listener = False))
		                                   
		self.shearPlot.tools.append(ZoomTool(self.shearPlot))
		self.shearPlot.tools.append(PanTool(self.shearPlot,drag_button='right'))
		
		self.shearPlot.title = 'Unclicked so far' + fileName
		leftPlot.add(self.shearPlot)
		rightPlot.add(self.normalPlot)

		
	traits_view = View(Item('hPlot',
										      editor = ComponentEditor(),
										      resizable = True,
										      show_label = False),
										 HGroup(Item('message',width = 400),
										        Item('cursorPosX',width = 400),
										        Item('cursorPosY',width = 400)),
										 buttons = [accept, reject, OKButton],
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
#!/usr/bin/env python

import matplotlib.pyplot as mpl
import numpy
import glob
import roxanne
import os.path

from enthought.traits.api import Int, HasTraits, Button
from enthought.traits.ui.api import View, Item
from enthought.traits.ui.menu import OKButton, CancelButton

class mathBox(HasTraits):
	plot = Instance(HPlotContainer)
	
	fileName = Str

	view = View('fileName',
	            buttons = [OKButton])
	            
	def __init__(self,x,y):
		self.a = x
		self.b = y
		self.c = x + y
		
	def _mult_fired(self):
		self.c = self.a * self.b
	
	def _a_changed(self):
		self.c = self.a + self.b
	
	def _b_changed(self):
		self.c = self.a + self.b
	
	view = View('a','b','c', 
	            Item('mult', show_label=False),
	            buttons = [OKButton, CancelButton])




fileNameList = glob.glob('*.data')
for fileName in fileNameList:

	myPlotBox = plotBox()
	myPlotBox.configure_traits()

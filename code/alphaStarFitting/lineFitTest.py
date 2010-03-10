#!/usr/bin/env python

from enthought.traits.api import HasTraits, Instance, Array, Range, Button, File
from enthought.traits.ui.api import View, Item, Handler
from enthought.traits.ui.menu import OKButton
from enthought.traits.ui.file_dialog import open_file
from enthought.traits.ui.key_bindings import KeyBinding, KeyBindings

from enthought.chaco.api import Plot, ArrayPlotData
from enthought.chaco.tools.api import RegressionLasso, RegressionOverlay

from enthought.enable.component_editor import ComponentEditor

from numpy import linspace, random,array

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
import roxanne as rx

class codeHandler(Handler):
    def test(self,info):
        print 'test'
        info.object._open_changed()
        
class dataView(HasTraits):
    x = Array
    y = Array

    traits_view = View(
                  Item('myPlot',
                       editor=ComponentEditor(),
                       show_label=False),
                  buttons = [OKButton],
                  resizable=True,
                  title='Window Title',
                  width=500,height=600)

    def __init__(self,fileName):
        self.getData(fileName)
        self.plotdata = ArrayPlotData(x=self.x,y=self.y)
        self.myPlot = Plot(self.plotdata)
        scatterplot = self.myPlot.plot(("x","y"),
                                       type="scatter", 
                                       color="blue")[0]
        self.myPlot.title = "Line Fit"
        
        # create regression tools
        regressionLasso = RegressionLasso(scatterplot, 
                          selection_datasource=scatterplot.index)
        regressionOverlay = RegressionOverlay(scatterplot, 
                            lasso_selection=regressionLasso)
                            
        # append regression tools to plot instance
        scatterplot.tools.append(regressionLasso)
        scatterplot.overlays.append(regressionOverlay)

    def getData(self,fileName):
        fileIn = open(fileName,'r')
        columnDict = rx.readDataFileArray(fileIn)
        shearForce = columnDict['forceMaxShear']
        normalForce = columnDict['forceMaxAdhesion']
        shearForce = array(shearForce,dtype=float)
        normalForce = array(normalForce,dtype=float)
        self.x = shearForce
        self.y = normalForce

class fileDialog(HasTraits):

    key_bindings = KeyBindings(
        KeyBinding (binding1 = 'o',
                    description = 'open',
                    method_name = 'test'),
                    )

    fileName = File
    open = Button('Open')
    view = View(Item('open'),Item('fileName',style='readonly'), 
                key_bindings = key_bindings,
                handler = codeHandler(),
                width=0.5)
    
    def _open_changed(self):
        fileName = open_file()
        if fileName != '':
            self.fileName = fileName
            viewer = dataView(fileName)
            viewer.configure_traits()            
            
if __name__ == '__main__':
    fileOpen = fileDialog()
    fileOpen.configure_traits()

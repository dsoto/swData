#!/usr/bin/env python

# simple interactive plot example using
# ComponentEditor and ArrayPlotData

from enthought.traits.api import HasTraits, Instance, Array, Range, Button
from enthought.traits.ui.api import View, Item
from enthought.chaco.api import Plot, ArrayPlotData
from enthought.enable.component_editor import ComponentEditor
from enthought.traits.ui.menu import OKButton
from numpy import linspace, random,array
from enthought.chaco.tools.api import RegressionLasso, RegressionOverlay

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
import roxanne as rx


class dataView(HasTraits):
    x = Array
    y = Array
    #slope = Range(low=-10,high=10.0,value=0.0)

    traits_view = View(
                  Item('myPlot',
                       editor=ComponentEditor(),
                       show_label=False),
     #             Item(name='slope'),
                  buttons = [OKButton],
                  resizable=True,
                  title='Window Title',
                  width=500,height=600)

    def __init__(self):

        self.getData()
        # data ranges
        #self.x = linspace(-10,10,100)
        #self.y = self.calc_y()

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

        '''
        def _slope_changed(self):
        self.y = self.calc_y()
        # set_data is necessary to update ArrayPlotData object
        # which then updates the plots
        self.plotdata.set_data("y",self.y)
        
        def calc_y(self):
        return self.slope*self.x + random.rand(100)
        '''

    def getData(self):
        pass
        fileName = 'FA-analyzed.data'
        fileIn = open(fileName,'r')
        columnDict = rx.readDataFileArray(fileIn)
        shearForce = columnDict['forceMaxShear']
        normalForce = columnDict['forceMaxAdhesion']
        shearForce = array(shearForce,dtype=float)
        normalForce = array(normalForce,dtype=float)
        print shearForce
        self.x = shearForce
        self.y = normalForce

        
if __name__ == '__main__':
    viewer = dataView()
    viewer.configure_traits()
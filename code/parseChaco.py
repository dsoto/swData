#!/usr/bin/env python

'''
fixme : put parsed*.dat file in directory with data
fixme : add keybinding to get return key to do OKButton
'''

from enthought.chaco.api               import (OverlayPlotContainer,
                                               VPlotContainer, Plot, ArrayPlotData)
from enthought.chaco.tools.api         import (PanTool, LineInspector)
from enthought.traits.api              import (HasTraits, Instance, Array,
                                               Button, Str, Int, Float, Bool, Tuple)
from enthought.traits.ui.api           import (View, Item, Handler, HGroup)
from enthought.traits.ui.menu          import Action, OKButton
from enthought.enable.component_editor import ComponentEditor
import numpy
import glob
import sys
import os.path
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
import roxanne as rx


class customTool(LineInspector):

    def __init__(self,*args,**kwargs):
        super(customTool,self).__init__(*args,**kwargs)
        self.plotBox = kwargs['plotBox']

    def normal_mouse_move(self, event):
        LineInspector.normal_mouse_move(self,event)
        plot = self.component
        plot.request_redraw()
        cursorPosX = self.component.map_data([event.x,event.y])[0]
        self.plotBox.cursorPosX = int(cursorPosX)
        self.plotBox.cursorPosY = self.plotBox.normal[self.plotBox.cursorPosX]

    def normal_left_down(self, event):
        cursorPosX = self.component.map_data([event.x,event.y])[0]
        self.plotBox.cursorPosX = int(cursorPosX)
        self.plotBox.cursorPosY = self.plotBox.normal[self.plotBox.cursorPosX]

        if self.plotBox.pointsClicked == 3:
            self.plotBox.pointsClicked = 0
        self.plotBox.pointX[self.plotBox.pointsClicked]=self.plotBox.cursorPosX
        self.plotBox.pointY[self.plotBox.pointsClicked]=self.plotBox.cursorPosY
        self.plotBox.pointX = self.plotBox.pointX
        self.plotBox.pointY = self.plotBox.pointY
        self.plotBox.plotdata.set_data('pointX',self.plotBox.pointX)
        self.plotBox.plotdata.set_data('pointY',self.plotBox.pointY)
        self.plotBox.pointsClicked += 1


    def normal_left_up(self, event):
        pass

class plotBoxHandler(Handler):

    def close(self, info, is_ok):
        if info.object.isAccepted == True:
            return True

    def closed(self, info, is_ok):
        outString = (info.object.fileName       + '\t' +
                     str(info.object.pointX[0]) + '\t' +
                     str(info.object.pointX[1]) + '\t' +
                     str(info.object.pointX[2]) + '\n')
        info.object.fOut.write(outString)
        info.object.fOut.flush()

    def accept(self, info):
        info.object.message = 'plot points accepted'
        info.object.isAccepted = True

    def reject(self, info):
        info.object.message = 'plot points rejected, choose again'
        info.object.pointX = numpy.array([0.0,100.0,200.0])
        info.object.pointY = numpy.array([0.0,0.0,0.0])
        info.object.plotdata.set_data('pointX',info.object.pointX)
        info.object.plotdata.set_data('pointY',info.object.pointY)
        info.object.isAccepted = False
        info.object.pointsClicked = 0

    def object_pointX_changed(self, info):
        pass

class plotBox(HasTraits):
    pointsClicked = Int
    index = Array
    normal = Array
    shear = Array
    pointX = Array(dtype = int, value = ([0.0,100.0,200.0]), comparison_mode = 0)
    pointY = Array(dtype = float, value = ([0.0,0.0,0.0]), comparison_mode = 0)
    message = Str
    fileTitle = Str
    isAccepted = Bool
    accept = Action(name = "Accept", action = "accept")
    reject = Action(name = "Reject", action = "reject")
    cursorPosX = Int
    cursorPosY = Float
    vPlot = Instance(VPlotContainer)

    def __init__(self, fileName, fOut):
        super(plotBox, self).__init__()

        self.isAccepted = True
        self.fOut = fOut
        self.message = 'Analysis Acceptable?'
        self.vPlot = VPlotContainer(padding = 10)
        self.vPlot.stack_order = 'top_to_bottom'
        topPlot = OverlayPlotContainer(padding = 10)
        self.vPlot.add(topPlot)
        bottomPlot = OverlayPlotContainer(padding = 10)
        self.vPlot.add(bottomPlot)

        # def parseFileName():
        self.fileName = fileName
        self.fileTitle = fileName
        # get complete path of data file
        fullFileName = os.path.abspath(fileName)
        self.fileName = os.path.split(fullFileName)[1]
        self.shortFileName = os.path.splitext(self.fileName)[1]
        self.plotTitle = self.shortFileName

        # def readData():
        fileIn = open(fileName,'r')
        hD = rx.readDataFileHeader(fileIn)
        dD = rx.readDataFileArray(fileIn)
        print dD.keys()

        #self.normal = numpy.array(map(float,dD['voltageForceNormal']))
        #self.shear  = numpy.array(map(float,dD['voltageForceLateral']))
        self.normal = numpy.array(map(float,dD['forceNormalMicroNewton']))
        self.shear  = numpy.array(map(float,dD['forceLateralMicroNewton']))
        self.index  = numpy.arange(len(self.normal))

        # index dictionary
        iD = rx.parseForceTrace(hD,dD)
        self.pointX[0] = iD['indexContact']
        self.pointY[0] = self.normal[iD['indexContact']]
        self.pointX[1] = iD['indexMaxPreload']
        self.pointY[1] = self.normal[iD['indexMaxPreload']]
        self.pointX[2] = iD['indexMaxAdhesion']
        self.pointY[2] = self.normal[iD['indexMaxAdhesion']]

        # def constructPlots():
        self.plotdata = ArrayPlotData(index = self.index,
                                      normal = self.normal,
                                      shear = self.shear,
                                      pointX = self.pointX,
                                      pointY = self.pointY)
        self.normalPlot = Plot(self.plotdata)
        self.normalPlot.plot(('index','normal'), type = 'line',
                                                 color = 'blue')
        self.normalPlot.plot(('pointX','pointY'), type = 'scatter',
                                                  marker = 'diamond',
                                                  marker_size = 5,
                                                  color = (0.0,0.0,1.0,0.5),
                                                  outline_color = 'none')

        # set y range of plot
        # self.normalPlot.value_range.set_bounds(-1,1)
        marginFactor = 1.1
        normalMaxRange = numpy.max(self.normal) * marginFactor
        normalMinRange = numpy.min(self.normal) * marginFactor
        self.normalPlot.value_range.set_bounds(normalMinRange, normalMaxRange)

        self.shearPlot = Plot(self.plotdata)
        self.shearPlot.plot(('index','shear'),type='line',color='green')

        self.normalPlot.overlays.append(customTool(plotBox = self,
                                           component = self.normalPlot,
                                           axis = 'index_x',
                                           inspect_mode = 'indexed',
                                           write_metadata = True,
                                           color = 'black',
                                           is_listener = False))

        self.normalPlot.tools.append(rx.SimpleZoom(self.normalPlot))
        self.normalPlot.tools.append(PanTool(self.normalPlot,drag_button = 'right'))

        self.normalPlot.title = 'Normal Force Trace'
        self.shearPlot.title  = 'Shear Force Trace'
        topPlot.add(self.shearPlot)
        bottomPlot.add(self.normalPlot)

        self.shearPlot.index_range = self.normalPlot.index_range

    traits_view = View(Item('vPlot',
                                              editor = ComponentEditor(),
                                              resizable = True,
                                              show_label = False),
                                         HGroup(Item('message',    width = 200),
                                                Item('cursorPosX', width = 200),
                                                Item('cursorPosY', width = 200),
                                                Item('pointX', style='readonly', width = 200),
                                                Item('pointY', style='readonly', width = 200)),
                                                Item('fileTitle', style = 'readonly', width = 200),
                                                buttons = [accept, reject, OKButton],
                     title = 'Roxanne Parse Application',
                     handler = plotBoxHandler(),
                     resizable = True,
                     width = 1400, height = 800,
                     x = 20, y = 40)

def main():
    # fileNameList = glob.glob('../20091124-sws10-ls/data/separated/p3*.data')
    # fileNameList = glob.glob('../20091124-sws11-ls/data/separated/p3*.data')
    # fileNameList=glob.glob('../030-20091230-sws15-ls/data/separated/p3*.data')
    fileNameList=glob.glob('../999-test-data/data/separated/*.data')

    timeStamp = rx.getTimeStamp()
    fOut = open('../999-test-data/data/parsed_' + timeStamp + '.dat', 'w')
    outputList = ['dataFileName',
                              'indexContact',
                              'indexMaxPreload',
                              'indexMaxAdhesion\n']
    sep = '\t'
    headerString = sep.join(outputList)
    fOut.write(headerString)

    numFiles = len(fileNameList)
    for i,fileName in enumerate(fileNameList):
        print fileName, i+1, ' in ', numFiles
        myPlotBox = plotBox(fileName,fOut)
        myPlotBox.configure_traits()


if __name__=='__main__':
    main()
#!/usr/bin/env python

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
        self.plotBox.pointIndex[self.plotBox.pointsClicked]=self.plotBox.cursorPosX
        self.plotBox.pointNormal[self.plotBox.pointsClicked]=self.plotBox.cursorPosY
        self.plotBox.pointShear[self.plotBox.pointsClicked]=self.plotBox.shear[self.plotBox.cursorPosX]
        self.plotBox.pointIndex = self.plotBox.pointIndex
        self.plotBox.pointNormal = self.plotBox.pointNormal
        self.plotBox.pointShear = self.plotBox.pointShear
        self.plotBox.plotdata.set_data('pointIndex',self.plotBox.pointIndex)
        self.plotBox.plotdata.set_data('pointNormal',self.plotBox.pointNormal)
        self.plotBox.plotdata.set_data('pointShear',self.plotBox.pointShear)
        self.plotBox.pointsClicked += 1


    def normal_left_up(self, event):
        pass

class plotBoxHandler(Handler):

    def close(self, info, is_ok):
        if info.object.isAccepted == True:
            return True

    def closed(self, info, is_ok):
        outString = (info.object.fileName       + '\t' +
                     str(info.object.pointIndex[0]) + '\t' +
                     str(info.object.pointIndex[1]) + '\t' +
                     str(info.object.pointIndex[2]) + '\n')
        info.object.fOut.write(outString)
        info.object.fOut.flush()

    def accept(self, info):
        info.object.message = 'plot points accepted'
        info.object.isAccepted = True

    def reject(self, info):
        info.object.message = 'plot points rejected, choose again'
        info.object.pointIndex = numpy.array([0.0,100.0,200.0])
        info.object.pointNormal = numpy.array([0.0,0.0,0.0])
        info.object.plotdata.set_data('pointIndex',info.object.pointIndex)
        info.object.plotdata.set_data('pointNormal',info.object.pointNormal)
        info.object.isAccepted = False
        info.object.pointsClicked = 0

    def object_pointIndex_changed(self, info):
        pass

class plotBox(HasTraits):
    pointsClicked = Int
    index = Array
    normal = Array
    shear = Array
    pointIndex = Array(dtype = int, value = ([0.0,100.0,200.0]), comparison_mode = 0)
    pointNormal = Array(dtype = float, value = ([0.0,0.0,0.0]), comparison_mode = 0)
    pointShear = Array(dtype = float, value = ([0.0,0.0,0.0]), comparison_mode = 0)
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

        #self.normal = numpy.array(map(float,dD['voltageForceNormal']))
        #self.shear  = numpy.array(map(float,dD['voltageForceLateral']))
        self.normal = numpy.array(map(float,dD['forceNormalMicroNewton']))
        self.shear  = numpy.array(map(float,dD['forceLateralMicroNewton']))
        self.index  = numpy.arange(len(self.normal))

        # index dictionary
        iD = rx.parseForceTrace(hD,dD)
        self.pointIndex[0] = iD['indexContact']
        self.pointIndex[1] = iD['indexMaxPreload']
        self.pointIndex[2] = iD['indexMaxAdhesion']

        self.pointNormal[0] = self.normal[iD['indexContact']]
        self.pointNormal[1] = self.normal[iD['indexMaxPreload']]
        self.pointNormal[2] = self.normal[iD['indexMaxAdhesion']]

        self.pointShear[0] = self.shear[iD['indexContact']]
        self.pointShear[1] = self.shear[iD['indexMaxPreload']]
        self.pointShear[2] = self.shear[iD['indexMaxAdhesion']]

        # def constructPlots():
        self.plotdata = ArrayPlotData(index = self.index,
                                      normal = self.normal,
                                      shear = self.shear,
                                      pointIndex = self.pointIndex,
                                      pointNormal = self.pointNormal,
                                      pointShear = self.pointShear)
        self.normalPlot = Plot(self.plotdata)
        self.normalPlot.plot(('index','normal'), type = 'line',
                                                 color = 'blue')
        self.normalPlot.plot(('pointIndex','pointNormal'), type = 'scatter',
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
        self.shearPlot.plot(('pointIndex','pointShear'), type = 'scatter',
                                                  marker = 'diamond',
                                                  marker_size = 5,
                                                  color = (0.0,0.0,1.0,0.5),
                                                  outline_color = 'none')

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

    w = 100
    traits_view = View(HGroup(Item('cursorPosX', width = w),
                              Item('cursorPosY', width = w)),
                       HGroup(Item('pointIndex', style='readonly', width = w)),
                       Item('fileTitle', style = 'readonly', width = w),
                       Item('vPlot',
                            editor = ComponentEditor(),
                            resizable = True,
                            show_label = False),
                       buttons = [accept, reject, OKButton],
                       title = 'Roxanne Parse Application',
                       handler = plotBoxHandler(),
                       resizable = True,
                       width = 600, height = 800,
                       x = 20, y = 40)

def main():
    directory = '../037-sps06-ls/'
    fileNameList=glob.glob(directory + 'data/separated/*.data')

    timeStamp = rx.getTimeStamp()
    fOut = open(directory + 'data/parsed_' + timeStamp + '.dat', 'w')
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
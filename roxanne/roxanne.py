#!/usr/bin/env python

from enthought.traits.api import HasTraits
from enthought.traits.api import Enum
from enthought.traits.api import HasTraits, Instance, Int, List
from enthought.enable.api import KeySpec
from enthought.chaco.api import AbstractOverlay
from enthought.enable.api import ColorTrait, KeySpec
from enthought.traits.api \
    import Bool, Enum, Float, Instance, Int, Str, Trait, Tuple

def main():
    print 'roxanne.py'
    return 0

def generateTrajectory():
    print 'generateTrajectory'
    # function outputvector = generateTrajectory(verticesMicron,velocityMicronPerSecond,pathFileName);
    #
    # % code to generate points for piezo movement
    #
    # % verticesMicron = M by 2 list of vertices
    # % velocityMicronPerSecond = M-1 by 1 list of velocities
    # % pathFileName = file name under which points are saved
    #
    #
    # % adds quiet period of zeros to start and end of trajectory data
    # addTails = true;
    # timeTareMSec = 100;
    # timeSettleMSec = 100;
    #
    # outdt = 1;   %time between output data points in milliseconds
    # acqdt = 1;    %time between acquired data points in milliseconds
    #
    # numlegs = length(velocityMicronPerSecond);
    #
    # path = [];
    # % put in initial series of zeros
    # numSteps = timeTareMSec / outdt;
    # tpath = zeros( numSteps, 2 );
    # path = [path; tpath];
    #
    # path = [path; verticesMicron(1,:)];    %adds starting point to the path
    # for i = 1:numlegs  % loop through coordinates vector
    #     d = sqrt( (verticesMicron(i+1,1) - verticesMicron(i,1))^2 + ...
    #               (verticesMicron(i+1,2) - verticesMicron(i,2))^2 );
    #     legtime = ( d/velocityMicronPerSecond(i) ) * 1000; %time in ms
    #     numsteps = ceil ( legtime / outdt );
    #     tpath = [ [1:numsteps]' [1:numsteps]' ];
    #     stepdist = (verticesMicron(i+1,:) - verticesMicron(i,:)) ./ numsteps;
    #     tpath(:,1) = stepdist(1) .* tpath(:,1) + verticesMicron(i,1);
    #     tpath(:,2) = stepdist(2) .* tpath(:,2) + verticesMicron(i,2);
    #     path = [path;tpath];
    # end
    #
    # % put in trailing series of zeros
    # numSteps = timeSettleMSec / outdt;
    # tpath = zeros( numSteps, 2 );
    # path = [path; tpath];
    #
    #
    # % output file
    # outputvector = [ outdt acqdt; path ];
    # filename = [ pathFileName '.traj' ];
    # fid = fopen(filename, 'wt');
    # fprintf(fid, '%-6.2f\t%-6.2f\n', outputvector');
    # fclose(fid);
    #
    # % show plot of trajectory
    # figure(1);
    # lov = size(outputvector,1);
    # plot(outputvector(2:lov,1),outputvector(2:lov,2),'b.');
    # title(pathFileName,'Interpreter','None');
    # xlabel('x-axis (micron)');
    # ylabel('y-axis (micron)');
    # axis([-10 100 -10 100]);
    # set(gca,'XDir','reverse');
    # set(gca,'YDir','reverse');
    # shg;
    print 'done'

def plotDataFileChacoPDF(fileName):
    import os.path
    import numpy

    baseFileName = os.path.splitext(fileName)
    baseFileName = baseFileName[0]
    plotFileName = baseFileName + 'Chaco.pdf'
    dataArray = readDataFile(fileName)
    time = dataArray[0]
    voltageNormal = dataArray[1]
    voltageShear = dataArray[2]
    positionX = dataArray[3]
    positionY = dataArray[4]
    x = numpy.arange(len(voltageNormal))

    from enthought.chaco.api import ArrayPlotData, Plot, PlotGraphicsContext
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
    gcpdf = PdfPlotGraphicsContext(filename=plotFileName,
                                dest_box=(0.5,0.5,5.0,5.0))
    gcpdf.render_component(p)
    gcpdf.save()

def plotDataFileChacoPNG(fileName):
    import os.path
    import numpy

    baseFileName = os.path.splitext(fileName)
    baseFileName = baseFileName[0]
    plotFileName = baseFileName + 'Chaco.png'
    dataArray = readDataFile(fileName)
    time = dataArray[0]
    voltageNormal = dataArray[1]
    voltageShear = dataArray[2]
    positionX = dataArray[3]
    positionY = dataArray[4]
    x = numpy.arange(len(voltageNormal))

    from enthought.traits.api import false
    from enthought.chaco.api import ArrayPlotData, Plot, PlotGraphicsContext
    from enthought.chaco.pdf_graphics_context import PdfPlotGraphicsContext

    pd=ArrayPlotData(index=x)
    p = Plot(pd,bgcolor="white",padding=50,border_visible=True)
    pd.set_data("normal",voltageNormal)
    pd.set_data("shear",voltageShear)
    p.plot(("index","normal"),color='blue',width=2.0)
    p.plot(("index","shear"),color='green',width=2.0)
    p.padding = 50
    p.title = baseFileName
    p.x_axis.title = "Sample"
    p.y_axis.title = "Voltage (V)"
    p.outer_bounds = ([800,600])
    p.do_layout(force=True)
    gcpng = PlotGraphicsContext(([800,600]),dpi=72)
    gcpng.render_component(p)
    gcpng.save(plotFileName)

def plotDataFileMPLPDF(fileName):
    import os.path
    import matplotlib.pyplot as plt
    
    baseFileName = os.path.splitext(fileName)
    baseFileName = baseFileName[0]
    print 'reading file ',fileName
    plotFileName = baseFileName + '.pdf'

    fileIn = open(fileName,'r')
    header = readDataFileHeader(fileIn)
    dataArray = readDataFileArray(fileIn)

    time = map(float,dataArray['time'])
    timeOffset = time[0]
    time = [x-timeOffset for x in time]
    voltageNormal = map(float,dataArray['voltageForceNormal'])
    voltageLateral = map(float,dataArray['voltageForceLateral'])
    #positionX = map(float,dataArray['voltagePositionX'])
    #positionY = map(float,dataArray['voltagePositionY'])

    figure = plt.figure()
    axesNormal  = figure.add_subplot(211)
    axesLateral = figure.add_subplot(212, sharex=axesNormal, sharey=axesNormal)
    
    # have to turn off TeX if i want to print the filename
    axesNormal.plot(time, voltageNormal, label='Normal Voltage', color='b')
    axesLateral.plot(time, voltageLateral, label='Lateral Voltage', color='g')
    #axes.plot(positionX, label='x position')
    #axes.plot(positionY, label='y position')
    axesLateral.set_xlabel('Time (sec)')
    axesLateral.set_ylabel('Piezo Voltage Signal (V)')
    axesNormal.set_ylabel('Piezo Voltage Signal (V)')
    axesNormal.grid(True,color=((0.5,0.5,0.5)))
    axesLateral.grid(True,color=((0.5,0.5,0.5)))
    
    # construct title for figure
    # have to escape underscores to accomodate TeX interpreter
    titleFileName = plotFileName.replace('_','\_')    
    figureTitle=(titleFileName)
    figureTitle += '\n' + 'cantilever = ' + header['cantilever']
    figureTitle += '\n' + 'sample = ' + header['sample']
    figure.suptitle(figureTitle)

    # set transparent legends
    l = axesLateral.legend()
    l.legendPatch.set_alpha(0.0)
    l = axesNormal.legend()
    l.legendPatch.set_alpha(0.0)
    
    
    width = 6
    height = 8
    figure.set_figheight(height)
    figure.set_figwidth(width)
    # figure.set_size_inches((width,height))

    figure.set_dpi(100)
    figure.savefig(plotFileName,transparent=True)
    
def plotDataFileForce(fileName):
    import os.path
    import matplotlib.pyplot as plt
    import numpy

    baseFileName = os.path.splitext(fileName)
    baseFileName = baseFileName[0]
    print 'reading file ',fileName
    plotFileName = baseFileName + '.pdf'

    fileIn = open(fileName,'r')
    headerDict = readDataFileHeader(fileIn)
    dataDict = readDataFileArray(fileIn)    
    
    time = map(float,dataDict['time'])
    timeOffset = time[0]
    time = [x-timeOffset for x in time]

    voltageLateral        =  map(float,dataDict['voltageForceLateral'])
    voltageNormal         =  map(float,dataDict['voltageForceNormal'])
    voltageLateral        = -numpy.array(voltageLateral)
    voltageNormal         =  numpy.array(voltageNormal)

    cantileverDict = getCantileverData(headerDict['cantilever'])

    normalStiffness      = cantileverDict['normalStiffness']
    lateralStiffness     = cantileverDict['lateralStiffness']
    normalDisplacement   = cantileverDict['normalDisplacement']
    lateralDisplacement  = cantileverDict['lateralDisplacement']
    lateralAmplification = float(headerDict['latAmp'])
    normalAmplification  = float(headerDict['norAmp'])

    defaultAmplification = 100
    lateralDisplacement = (lateralDisplacement * lateralAmplification /
                                                 defaultAmplification)
    normalDisplacement = (normalDisplacement * normalAmplification /
                                              defaultAmplification)

    # use cantilever values to convert voltages to forces
    lateralForceMuN = (voltageLateral *
                               lateralStiffness / lateralDisplacement)
    normalForceMuN  = (voltageNormal * normalStiffness /
                               normalDisplacement)    

    figure = plt.figure()
    axesNormal  = figure.add_subplot(211)
    axesLateral = figure.add_subplot(212, sharex=axesNormal, sharey=axesNormal)
    
    # have to turn off TeX if i want to print the filename
    axesNormal.plot(time, normalForceMuN, 
                    label='Normal Force ($\mu$N)', color='b')
    axesLateral.plot(time, lateralForceMuN, 
                    label='Lateral Force ($\mu$N)', color='g')
    axesLateral.set_xlabel('Time (sec)')
    axesLateral.set_ylabel('Lateral Force ($\mu$N)')
    axesNormal.set_ylabel('Normal Force ($\mu$N)')
    axesNormal.grid(True,color=((0.5,0.5,0.5)))
    axesLateral.grid(True,color=((0.5,0.5,0.5)))
    
    # construct title for figure
    # have to escape underscores to accomodate TeX interpreter
    titleFileName = plotFileName.replace('_','\_')    
    figureTitle=(titleFileName)
    figureTitle += '\n' + 'cantilever = ' + headerDict['cantilever']
    figureTitle += '\n' + 'sample = ' + headerDict['sample']
    figure.suptitle(figureTitle)

    # set transparent legends
    l = axesLateral.legend()
    l.legendPatch.set_alpha(0.0)
    l = axesNormal.legend()
    l.legendPatch.set_alpha(0.0)
    
    
    width = 6
    height = 8
    figure.set_figheight(height)
    figure.set_figwidth(width)
    # figure.set_size_inches((width,height))

    figure.set_dpi(100)
    figure.savefig(plotFileName,transparent=True)



def addToDict(kvDict, key, tempLine):
    index = tempLine.find('=')+1
    length = len(tempLine)
    val = tempLine[index-length:]
    val = val.lstrip()
    kvDict.update({key:val})
    return kvDict

def getCantileverData(cantilever):
    cantileverDict = {}
    if cantilever == '529b02':
        lateralStiffness    = 3.898
        normalStiffness     = 0.659
        lateralDisplacement = 1.148
        normalDisplacement  = 0.224

    if cantilever == '629a03':
        lateralStiffness    = 0.307
        normalStiffness     = 0.313
        lateralDisplacement = 0.473
        normalDisplacement  = 0.148

    cantileverDict['lateralStiffness']    = lateralStiffness
    cantileverDict['normalStiffness']     = normalStiffness
    cantileverDict['lateralDisplacement'] = lateralDisplacement
    cantileverDict['normalDisplacement']  = normalDisplacement

    return cantileverDict

def readDataFileHeader(fileIn):
    # read in file
    # read in lines until find data tag
    # if line contains '=' put entries in dictionary

    kvDict = {}
    keepReading = 1
    while keepReading == 1:
        tempLine = fileIn.readline()
        tempLine = tempLine.lower()
        tempLine = tempLine.rstrip()

        if tempLine.find('normal') != -1:
            key = 'norAmp'
            kvDict = addToDict(kvDict, key, tempLine)
        if tempLine.find('lateral') != -1:
            key = 'latAmp'
            kvDict = addToDict(kvDict, key, tempLine)
        if tempLine.find('roll') != -1:
            key = 'rollAngle'
            kvDict = addToDict(kvDict, key, tempLine)
        if tempLine.find('pitch') != -1:
            key = 'pitchAngle'
            kvDict = addToDict(kvDict, key, tempLine)
        if tempLine.find('cantilever') != -1:
            key = 'cantilever'
            kvDict = addToDict(kvDict, key, tempLine)
        if tempLine.find('sample') != -1:
            key = 'sample'
            kvDict = addToDict(kvDict, key, tempLine)

        if tempLine.find('<data>')!=-1:
            keepReading = 0

    return kvDict

def readDataFileArray(fileIn):

    tempLine = fileIn.readline()
    tempLine = tempLine.rstrip()
    headers = tempLine.split('\t')

    # TODO : strip whitespace from headers

    numColumns = len(headers)

    columnList = []
    for i in range(numColumns):
        columnList.append([])

    tempData = fileIn.readlines()

    # loop through data and append arrays
    for line in tempData:
        #line = line.replace('\n','')
        line = line.rstrip('\r\n')
        line = line.replace('\r','')
        value = line.split('\t')
        for i in range(numColumns):
            columnList[i].append(value[i])

    columnDict = {}
    for i in range(numColumns):
        columnDict[headers[i]] = columnList[i]

    # tidy up and return values
    fileIn.close()
    return columnDict

def parseForceTrace(hD,dD):

    import matplotlib.pyplot as mpl
    import numpy      as np
    import sys

    voltageLateral        =  map(float,dD['voltageForceLateral'])
    voltageNormal         =  map(float,dD['voltageForceNormal'])
    positionNormalMicron  =  map(float,dD['voltagePositionX']) * 10
    positionLateralMicron =  map(float,dD['voltagePositionY']) * 10

    voltageLateral        = -np.array(voltageLateral)
    voltageNormal         =  np.array(voltageNormal)
    positionNormalMicron  =  np.array(positionNormalMicron) * 10
    positionLateralMicron =  np.array(positionLateralMicron) * 10

    # cantilever dictionary
    cD = getCantileverData(hD['cantilever'])

    normalStiffness      = cD['normalStiffness']
    lateralStiffness     = cD['lateralStiffness']
    normalDisplacement   = cD['normalDisplacement']
    lateralDisplacement  = cD['lateralDisplacement']

    # filter spikes
    
    # finding points of interest
    # 03 june 2009 - changing to be more robust
    # idea is to find maximum value -> preload
    # then find next local minimum, that is pulloff
    
    # original algorithm
    #indexMaxAdhesion = np.argmin(voltageNormal)
    #indexMaxPreload = np.argmax(voltageNormal[0:indexMaxAdhesion+1])
    #indexContact = np.argmin(voltageNormal[0:indexMaxPreload+1])

    indexMaxPreload = np.argmax(voltageNormal)
    indexMaxAdhesion = 0 # here find local min
    forwardWindow = 8
    backwardWindow = 2
    for i in range(indexMaxPreload+backwardWindow, 
                   len(voltageNormal)-forwardWindow):
        #if np.average(voltageNormal[i-backwardWindow:i-1])>voltageNormal[i] and np.average(voltageNormal[i+3:i+forwardWindow])>voltageNormal[i]:
        if np.average(voltageNormal[i-backwardWindow:i])>voltageNormal[i] and np.average(voltageNormal[i:i+forwardWindow])>voltageNormal[i]:
            indexMaxAdhesion = i+3
            break
    indexContact = np.argmin(voltageNormal[0:indexMaxPreload+1])
    
    index = {'indexContact'     : indexContact,
             'indexMaxPreload'  : indexMaxPreload,
             'indexMaxAdhesion' : indexMaxAdhesion}
    return index

def getTimeStamp():
    from datetime import datetime
    dt = datetime.now()
    return dt.strftime('%Y%m%d_%H%M')

# numpy import must be outside to work
from numpy import allclose, inf
class BaseZoomTool(HasTraits):
    """ Defines traits and methods to actually perform the logic of zooming
    onto a plot.
    """

    from enthought.traits.api import Float
    # If the tool only applies to a particular axis, this attribute is used to
    # determine which mapper and range to use.
    axis = Enum("index", "value")

    # The maximum ratio between the original data space bounds and the zoomed-in
    # data space bounds.  If None, then there is no limit (not advisable!).
    max_zoom_in_factor = Float(1e5, allow_none=True)

    # The maximum ratio between the zoomed-out data space bounds and the original
    # bounds.  If None, then there is no limit.
    max_zoom_out_factor = Float(1e5, allow_none=True)

    def _zoom_limit_reached(self, orig_low, orig_high, new_low, new_high, mapper=None):
        """ Returns True if the new low and high exceed the maximum zoom
        limits
        """
        orig_bounds = orig_high - orig_low

        if orig_bounds == inf:
            # There isn't really a good way to handle the case when the
            # original bounds were infinite, since any finite zoom
            # range will certainly exceed whatever zoom factor is set.
            # If this is the case, we skip the zoom factor checks,
            # and move on to the domain limits checks
            pass
        else:
            new_bounds = new_high - new_low
            if allclose(orig_bounds, 0.0):
                return True
            if allclose(new_bounds, 0.0):
                return True
            if (new_bounds / orig_bounds) > self.max_zoom_out_factor or \
               (orig_bounds / new_bounds) > self.max_zoom_in_factor:
                return True

        return False

    #------------------------------------------------------------------------
    # Utility methods for computing axes, coordinates, etc.
    #------------------------------------------------------------------------

    def _get_mapper(self):
        """ Returns the mapper for the component associated with this tool.

        The zoom tool really only cares about this, so subclasses can easily
        customize SimpleZoom to work with all sorts of components just by
        overriding this method.
        """
        if self.component is not None:
            return getattr(self.component, self.axis + "_mapper")
        else:
            return None


    def _get_axis_coord(self, event, axis="index"):
        """ Returns the coordinate of the event along the axis of interest
        to the tool (or along the orthogonal axis, if axis="value").
        """
        event_pos = (event.x, event.y)
        if axis == "index":
            return event_pos[ self._determine_axis() ]
        else:
            return event_pos[ 1 - self._determine_axis() ]

    def _determine_axis(self):
        """ Determines whether the index of the coordinate along the axis of
        interest is the first or second element of an (x,y) coordinate tuple.
        """
        if self.axis == "index":
            if self.component.orientation == "h":
                return 0
            else:
                return 1
        else:   # self.axis == "value"
            if self.component.orientation == "h":
                return 1
            else:
                return 0

    def _map_coordinate_box(self, start, end):
        """ Given start and end points in screen space, returns corresponding
        low and high points in data space.
        """
        low = [0,0]
        high = [0,0]
        for axis_index, mapper in [(0, self.component.x_mapper), \
                                   (1, self.component.y_mapper)]:
            low_val = mapper.map_data(start[axis_index])
            high_val = mapper.map_data(end[axis_index])

            if low_val > high_val:
                low_val, high_val = high_val, low_val
            low[axis_index] = low_val
            high[axis_index] = high_val
        return low, high

class ToolHistoryMixin(HasTraits):
    """ A mix-in class for tools to maintain a tool state history and to move
    backwards and forwards through that history stack.

    This mix-in listens for keypressed events; to handle keypresses in a
    subclass, call self._history_handle_key(event) to have this mix-in properly
    process the event.
    """

    # Key to go to the original or start state in the history.
    reset_state_key = Instance(KeySpec, args=("Esc",))

    # Key to go to the previous state in the history.
    prev_state_key = Instance(KeySpec, args=("Left", "control"))

    # Key to go to the next state in the history.
    next_state_key = Instance(KeySpec, args=("Right", "control"))

    # The state stack.
    _history = List

    # The current index into _history
    _history_index = Int

    #------------------------------------------------------------------------
    # Abstract methods that subclasses must implement to handle keypresses
    #------------------------------------------------------------------------

    def _next_state_pressed(self):
        """ Called when the tool needs to advance to the next state in the
        stack.

        The **_history_index** will have already been set to the index
        corresponding to the next state.
        """
        pass

    def _prev_state_pressed(self):
        """ Called when the tool needs to advance to the previous state in the
        stack.

        The **_history_index** will have already been set to the index
        corresponding to the previous state.
        """
        pass

    def _reset_state_pressed(self):
        """ Called when the tool needs to reset its history.

        The history index will have already been set to 0.
        """
        pass


    #------------------------------------------------------------------------
    # Protected methods for subclasses to use
    #------------------------------------------------------------------------

    def _current_state(self):
        """ Returns the current history state.
        """
        return self._history[self._history_index]

    def _reset_state(self, state):
        """ Clears the history stack and sets the first or original state in
        the history to *state*.
        """
        self._history = [state]
        self._history_index = 0
        return

    def _append_state(self, state, set_index=True):
        """ Clears the history after the current **_history_index**, and
        appends the given state to the history.

        If *set_index* is True, the method sets the **_history_index** to
        match the new, truncated history. If it is False, the history index
        is unchanged.
        """
        new_history = self._history[:self._history_index+1] + [state]
        self._history = new_history
        if set_index:
            self._history_index = len(self._history) - 1
        return

    def _pop_state(self):
        """ Pops the most last state off the history stack.

        If the history index points to the end of the stack, then it is
        adjusted; otherwise, the index is unaffected. If the stack is empty,
        the method raises an IndexError.

        Returns the popped state.
        """
        if len(self._history) == 0:
            raise IndexError("Unable to pop empty history stack.")

        if self._history_index == len(self._history) - 1:
            self._history_index -= 1

        return self._history.pop()

    #------------------------------------------------------------------------
    # Private methods / event handlers
    #------------------------------------------------------------------------

    def normal_key_pressed(self, event):
        """ Handles a key being pressed, and takes appropriate action if it is
        one of the history keys defined for this class.
        """
        self._history_handle_key(event)
        return

    def _history_handle_key(self, event):
        if self.reset_state_key.match(event):
            self._history_index = 0
            self._reset_state_pressed()
            event.handled = True
        elif self.prev_state_key.match(event):
            if self._history_index > 0:
                self._history_index -= 1
                self._prev_state_pressed()
            event.handled = True
        elif self.next_state_key.match(event):
            if self._history_index <= len(self._history) - 2:
                self._history_index += 1
                self._next_state_pressed()
            event.handled = True
        else:
            return

class SimpleZoom(AbstractOverlay, ToolHistoryMixin, BaseZoomTool):
    """ Selects a range along the index or value axis.

    The user left-click-drags to select a region to zoom in.
    Certain keyboard keys are mapped to performing zoom actions as well.

    Implements a basic "zoom stack" so the user move go backwards and forwards
    through previous zoom regions.
    """
    from numpy import array
    # The selection mode:
    #
    # range:
    #   Select a range across a single index or value axis.
    # box:
    #   Perform a "box" selection on two axes.
    tool_mode = Enum("box", "range")

    # Is the tool always "on"? If True, left-clicking always initiates
    # a zoom operation; if False, the user must press a key to enter zoom mode.
    always_on = Bool(False)

    #-------------------------------------------------------------------------
    # Zoom control
    #-------------------------------------------------------------------------

    # The axis to which the selection made by this tool is perpendicular. This
    # only applies in 'range' mode.
    axis = Enum("index", "value")

    #-------------------------------------------------------------------------
    # Interaction control
    #-------------------------------------------------------------------------

    # Enable the mousewheel for zooming?
    enable_wheel = Bool(True)

    # The mouse button that initiates the drag.  If "None", then the tool
    # will not respond to drag.  (It can still respond to mousewheel events.)
    drag_button = Enum("left", "right", None)

    # Conversion ratio from wheel steps to zoom factors.
    wheel_zoom_step = Float(1.0)

    # The key press to enter zoom mode, if **always_on** is False.  Has no effect
    # if **always_on** is True.
    enter_zoom_key = Instance(KeySpec, args=("z",))

    # The key press to leave zoom mode, if **always_on** is False.  Has no effect
    # if **always_on** is True.
    exit_zoom_key = Instance(KeySpec, args=("z",))

    # Disable the tool after the zoom is completed?
    disable_on_complete = Bool(True)

    # The minimum amount of screen space the user must select in order for
    # the tool to actually take effect.
    minimum_screen_delta = Int(10)

    #-------------------------------------------------------------------------
    # Appearance properties (for Box mode)
    #-------------------------------------------------------------------------

    # The pointer to use when drawing a zoom box.
    pointer = "magnifier"

    # The color of the selection box.
    color = ColorTrait("lightskyblue")

    # The alpha value to apply to **color** when filling in the selection
    # region.  Because it is almost certainly useless to have an opaque zoom
    # rectangle, but it's also extremely useful to be able to use the normal
    # named colors from Enable, this attribute allows the specification of a
    # separate alpha value that replaces the alpha value of **color** at draw
    # time.
    alpha = Trait(0.4, None, Float)

    # The color of the outside selection rectangle.
    border_color = ColorTrait("dodgerblue")

    # The thickness of selection rectangle border.
    border_size = Int(1)

    # The possible event states of this zoom tool.
    event_state = Enum("normal", "selecting")

    #------------------------------------------------------------------------
    # Key mappings
    #------------------------------------------------------------------------

    # The key that cancels the zoom and resets the view to the original defaults.
    cancel_zoom_key = Instance(KeySpec, args=("Esc",))

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    # If **always_on** is False, this attribute indicates whether the tool
    # is currently enabled.
    _enabled = Bool(False)

    # the original numerical screen ranges
    _orig_low_setting = Trait(None, Tuple, Float, Str)
    _orig_high_setting = Trait(None, Tuple, Float, Str)

    # The (x,y) screen point where the mouse went down.
    _screen_start = Trait(None, None, Tuple)

    # The (x,,y) screen point of the last seen mouse move event.
    _screen_end = Trait(None, None, Tuple)

    def __init__(self, component=None, *args, **kw):
        # Support AbstractController-style constructors so that this can be
        # handed in the component it will be overlaying in the constructor
        # without using kwargs.
        self.component = component
        super(SimpleZoom, self).__init__(*args, **kw)
        self._reset_state_to_current()
        if self.tool_mode == "range":
            mapper = self._get_mapper()
            self._orig_low_setting = mapper.range.low_setting
            self._orig_high_setting = mapper.range.high_setting
        else:
            x_range = self.component.x_mapper.range
            y_range = self.component.y_mapper.range
            self._orig_low_setting = (x_range.low_setting, y_range.low_setting)
            self._orig_high_setting = \
                (x_range.high_setting, y_range.high_setting)
        component.on_trait_change(self._reset_state_to_current,
                                  "index_data_changed")
        return

    def enable(self, event=None):
        """ Provides a programmatic way to enable this tool, if
        **always_on** is False.

        Calling this method has the same effect as if the user pressed the
        **enter_zoom_key**.
        """
        if self.component.active_tool != self:
            self.component.active_tool = self
        self._enabled = True
        if event and event.window:
            event.window.set_pointer(self.pointer)
        return

    def disable(self, event=None):
        """ Provides a programmatic way to enable this tool, if **always_on**
        is False.

        Calling this method has the same effect as if the user pressed the
        **exit_zoom_key**.
        """
        self.reset()
        self._enabled = False
        if self.component.active_tool == self:
            self.component.active_tool = None
        if event and event.window:
            event.window.set_pointer("arrow")
        return

    def reset(self, event=None):
        """ Resets the tool to normal state, with no start or end position.
        """
        self.event_state = "normal"
        self._screen_start = None
        self._screen_end = None

    def deactivate(self, component):
        """ Called when this is no longer the active tool.
        """
        # Required as part of the AbstractController interface.
        return self.disable()

    def overlay(self, component, gc, view_bounds=None, mode="normal"):
        """ Draws this component overlaid on another component.

        Overrides AbstractOverlay.
        """
        if self.event_state == "selecting":
            if self.tool_mode == "range":
                self.overlay_range(component, gc)
            else:
                self.overlay_box(component, gc)
        return

    def overlay_box(self, component, gc):
        """ Draws the overlay as a box.
        """
        if self._screen_start and self._screen_end:
            gc.save_state()
            try:
                gc.set_antialias(0)
                gc.set_line_width(self.border_size)
                gc.set_stroke_color(self.border_color_)
                gc.clip_to_rect(component.x, component.y, component.width, component.height)
                x, y = self._screen_start
                x2, y2 = self._screen_end
                rect = (x, y, x2-x+1, y2-y+1)
                if self.color != "transparent":
                    if self.alpha:
                        color = list(self.color_)
                        if len(color) == 4:
                            color[3] = self.alpha
                        else:
                            color += [self.alpha]
                    else:
                        color = self.color_
                    gc.set_fill_color(color)
                    gc.rect(*rect)
                    gc.draw_path()
                else:
                    gc.rect(*rect)
                    gc.stroke_path()
            finally:
                gc.restore_state()
        return

    def overlay_range(self, component, gc):
        """ Draws the overlay as a range.
        """
        axis_ndx = self._determine_axis()
        lower_left = [0,0]
        upper_right = [0,0]
        lower_left[axis_ndx] = self._screen_start[axis_ndx]
        lower_left[1-axis_ndx] = self.component.position[1-axis_ndx]
        upper_right[axis_ndx] = self._screen_end[axis_ndx] - self._screen_start[axis_ndx]
        upper_right[1-axis_ndx] = self.component.bounds[1-axis_ndx]

        gc.save_state()
        try:
            gc.set_antialias(0)
            gc.set_alpha(self.alpha)
            gc.set_fill_color(self.color_)
            gc.set_stroke_color(self.border_color_)
            gc.clip_to_rect(component.x, component.y, component.width, component.height)
            gc.rect(lower_left[0], lower_left[1], upper_right[0], upper_right[1])
            gc.draw_path()
        finally:
            gc.restore_state()
        return

    def normal_left_down(self, event):
        """ Handles the left mouse button being pressed while the tool is
        in the 'normal' state.

        If the tool is enabled or always on, it starts selecting.
        """
        if self.always_on or self._enabled:
            # we need to make sure that there isn't another active tool that we will
            # interfere with.
            if self.drag_button == "left":
                self._start_select(event)
        return

    def normal_right_down(self, event):
        """ Handles the right mouse button being pressed while the tool is
        in the 'normal' state.

        If the tool is enabled or always on, it starts selecting.
        """
        if self.always_on or self._enabled:
            if self.drag_button == "right":
                self._start_select(event)
        return

    def selecting_mouse_move(self, event):
        """ Handles the mouse moving when the tool is in the 'selecting' state.

        The selection is extended to the current mouse position.
        """
        self._screen_end = (event.x, event.y)
        self.component.request_redraw()
        event.handled = True
        return

    def selecting_left_up(self, event):
        """ Handles the left mouse button being released when the tool is in
        the 'selecting' state.

        Finishes selecting and does the zoom.
        """
        if self.drag_button == "left":
            self._end_select(event)
        return

    def selecting_right_up(self, event):
        """ Handles the right mouse button being released when the tool is in
        the 'selecting' state.

        Finishes selecting and does the zoom.
        """
        if self.drag_button == "right":
            self._end_select(event)
        return

    def selecting_mouse_leave(self, event):
        """ Handles the mouse leaving the plot when the tool is in the
        'selecting' state.

        Ends the selection operation without zooming.
        """
        self._end_selecting(event)
        return

    def selecting_key_pressed(self, event):
        """ Handles a key being pressed when the tool is in the 'selecting'
        state.

        If the key pressed is the **cancel_zoom_key**, then selecting is
        canceled.
        """
        if self.cancel_zoom_key.match(event):
            self._end_selecting(event)
            event.handled = True
        return

    def _start_select(self, event):
        """ Starts selecting the zoom region
        """
        if self.component.active_tool in (None, self):
            self.component.active_tool = self
        else:
            self._enabled = False
        self._screen_start = (event.x, event.y)
        self._screen_end = None
        self.event_state = "selecting"
        event.window.set_pointer(self.pointer)
        event.window.set_mouse_owner(self, event.net_transform())
        self.selecting_mouse_move(event)
        return

    def _end_select(self, event):
        """ Ends selection of the zoom region, adds the new zoom range to
        the zoom stack, and does the zoom.
        """
        self._screen_end = (event.x, event.y)

        start = array(self._screen_start)
        end = array(self._screen_end)

        if sum(abs(end - start)) < self.minimum_screen_delta:
            self._end_selecting(event)
            event.handled = True
            return

        if self.tool_mode == "range":
            mapper = self._get_mapper()
            axis = self._determine_axis()
            low = mapper.map_data(self._screen_start[axis])
            high = mapper.map_data(self._screen_end[axis])

            if low > high:
                low, high = high, low
        else:
            low, high = self._map_coordinate_box(self._screen_start, self._screen_end)

        new_zoom_range = (low, high)
        self._append_state(new_zoom_range)
        self._do_zoom()
        self._end_selecting(event)
        event.handled = True
        return

    def _end_selecting(self, event=None):
        """ Ends selection of zoom region, without zooming.
        """
        if self.disable_on_complete:
            self.disable(event)
        else:
            self.reset()
        self.component.request_redraw()
        if event and event.window.mouse_owner == self:
            event.window.set_mouse_owner(None)
        return

    def _do_zoom(self):
        """ Does the zoom operation.
        """
        # Sets the bounds on the component using _cur_stack_index
        low, high = self._current_state()
        orig_low, orig_high = self._history[0]

        if self._history_index == 0:
            if self.tool_mode == "range":
                mapper = self._get_mapper()
                mapper.range.low_setting = self._orig_low_setting
                mapper.range.high_setting = self._orig_high_setting
            else:
                x_range = self.component.x_mapper.range
                y_range = self.component.y_mapper.range
                x_range.low_setting, y_range.low_setting = \
                    self._orig_low_setting
                x_range.high_setting, y_range.high_setting = \
                    self._orig_high_setting

                # resetting the ranges will allow 'auto' to pick the values
                x_range.reset()
                y_range.reset()

        else:
            if self.tool_mode == "range":
                mapper = self._get_mapper()
                if self._zoom_limit_reached(orig_low, orig_high, low, high, mapper):
                    self._pop_state()
                    return
                mapper.range.low = low
                mapper.range.high = high
            else:
                for ndx in (0, 1):
                    mapper = (self.component.x_mapper, self.component.y_mapper)[ndx]
                    if self._zoom_limit_reached(orig_low[ndx], orig_high[ndx],
                                                low[ndx], high[ndx], mapper):
                        # pop _current_state off the stack and leave the actual
                        # bounds unmodified.
                        self._pop_state()
                        return
                x_range = self.component.x_mapper.range
                y_range = self.component.y_mapper.range
                x_range.low, y_range.low = low
                x_range.high, y_range.high = high

        self.component.request_redraw()
        return

    def normal_key_pressed(self, event):
        """ Handles a key being pressed when the tool is in 'normal' state.

        If the tool is not always on, this method handles turning it on and
        off when the appropriate keys are pressed. Also handles keys to
        manipulate the tool history.
        """
        if not self.always_on:
            if not self._enabled and self.enter_zoom_key.match(event):
                if self.component.active_tool in (None, self):
                    self.component.active_tool = self
                    self._enabled = True
                    event.window.set_pointer(self.pointer)
                else:
                    self._enabled = False
                return
            elif self._enabled and self.exit_zoom_key.match(event):
                self._enabled = False
                event.window.set_pointer("arrow")
                return

        self._history_handle_key(event)

        if event.handled:
            self.component.request_redraw()
        return

    def normal_mouse_wheel(self, event):
        """ Handles the mouse wheel being used when the tool is in the 'normal'
        state.

        Scrolling the wheel "up" zooms in; scrolling it "down" zooms out.
        """
        if self.enable_wheel and event.mouse_wheel != 0:
            if event.mouse_wheel > 0:
                # zoom in
                zoom = 1.0 / (1.0 + 0.5 * self.wheel_zoom_step)
            elif event.mouse_wheel < 0:
                # zoom out
                zoom = 1.0 + 0.5 * self.wheel_zoom_step

            # We'll determine the current position of the cursor in screen coordinates,
            # and only afterwards map to dataspace.
            c = self.component
            screenlow_pt, screenhigh_pt = (c.x, c.y), (c.x2, c.y2)
            mouse_pos = (event.x, event.y)

            if self.tool_mode == "range":
                mapper_list = [(self._determine_axis(), self._get_mapper())]
            else:
                mapper_list = [(0, c.x_mapper), (1, c.y_mapper)]

            orig_low, orig_high = self._history[0]

            # If any of the axes reaches its zoom limit, we should cancel the zoom.
            # We should first calculate the new ranges and store them. If none of
            # the axes reach zoom limit, we can apply the new ranges.
            todo_list = []
            for ndx, mapper in mapper_list:
                screenrange = mapper.screen_bounds
                mouse_val = mouse_pos[ndx]
                newscreenlow = mouse_val + zoom * (screenlow_pt[ndx] - mouse_val)
                newscreenhigh = mouse_val + zoom * (screenhigh_pt[ndx] - mouse_val)

                newlow = mapper.map_data(newscreenlow)
                newhigh = mapper.map_data(newscreenhigh)

                if type(orig_high) in (tuple,list):
                    ol, oh = orig_low[ndx], orig_high[ndx]
                else:
                    ol, oh = orig_low, orig_high

                if self._zoom_limit_reached(ol, oh, newlow, newhigh, mapper):
                    # Ignore other axes, we're done.
                    event.handled = True
                    return
                if ndx == 0:
                    todo_list.append((mapper,newlow,newhigh))

            # Check the domain limits on each dimension, and rescale the zoom
            # amount if necessary.
            for ndx, (mapper, newlow, newhigh) in enumerate(todo_list):
                domain_min, domain_max = getattr(mapper, "domain_limits", (None,None))
                if domain_min is not None and newlow < domain_min:
                    newlow = domain_min
                if domain_max is not None and newhigh > domain_max:
                    newhigh = domain_max
                todo_list[ndx] = (mapper, newlow, newhigh)

            # All axes can be rescaled, do it.
            for mapper, newlow, newhigh in todo_list:
                if newlow > newhigh:
                    newlow, newhigh = newhigh, newlow
                mapper.range.set_bounds(newlow, newhigh)

            event.handled = True
            c.request_redraw()
        return

    def _component_changed(self):
        if self._get_mapper() is not None:
            self._reset_state_to_current()
        return

    #------------------------------------------------------------------------
    # Implementation of PlotComponent interface
    #------------------------------------------------------------------------

    def _activate(self):
        """ Called by PlotComponent to set this as the active tool.
        """
        self.enable()

    #------------------------------------------------------------------------
    # implementations of abstract methods on ToolHistoryMixin
    #------------------------------------------------------------------------

    def _reset_state_to_current(self):
        """ Clears the tool history, and sets the current state to be the
        first state in the history.
        """
        if self.tool_mode == "range":
            mapper = self._get_mapper()
            if mapper is not None:
                self._reset_state((mapper.range.low,
                                   mapper.range.high))
        else:
            if self.component.x_mapper is not None:
                x_range = self.component.x_mapper.range
                xlow = x_range.low
                xhigh = x_range.high
            else:
                xlow = "auto"
                xhigh = "auto"

            if self.component.y_mapper is not None:
                y_range = self.component.y_mapper.range
                ylow = y_range.low
                yhigh = y_range.high
            else:
                ylow = "auto"
                yhigh = "auto"

            self._reset_state(((xlow, ylow),
                               (xhigh, yhigh)))

    def _reset_state_pressed(self):
        """ Called when the tool needs to reset its history.

        The history index will have already been set to 0. Implements
        ToolHistoryMixin.
        """
        # First zoom to the set state (ZoomTool handles setting the index=0).
        self._do_zoom()

        # Now reset the state to the current bounds settings.
        self._reset_state_to_current()
        return

    def _prev_state_pressed(self):
        """ Called when the tool needs to advance to the previous state in the
        stack.

        The history index will have already been set to the index corresponding
        to the prev state. Implements ToolHistoryMixin.
        """
        self._do_zoom()
        return

    def _next_state_pressed(self):
        """ Called when the tool needs to advance to the next state in the stack.

        The history index will have already been set to the index corresponding
        to the next state. Implements ToolHistoryMixin.
        """
        self._do_zoom()
        return

    ### Persistence ###########################################################

    def __getstate__(self):
        dont_pickle = [
            'always_on',
            'enter_zoom_key',
            'exit_zoom_key',
            'minimum_screen_delta',
            'event_state',
            'reset_zoom_key',
            'prev_zoom_key',
            'next_zoom_key',
            'pointer',
            '_enabled',
            '_screen_start',
            '_screen_end']
        state = super(SimpleZoom,self).__getstate__()
        for key in dont_pickle:
            if state.has_key(key):
                del state[key]

        return state

# deprecated methods below
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

#!/usr/bin/env python

# plotting script that expects a header line with labels for 
# each column of data
# these columns of data will be assigned to a dictionary
# returned values are all strings
from enthought.traits.api import HasTraits, Instance, Array, Range, Button, File
from enthought.traits.ui.api import View, Item, Handler
from enthought.traits.ui.menu import OKButton
from enthought.traits.ui.file_dialog import open_file

import sys
sys.path.append('/Users/dsoto/current/swDataFlat/roxanne')
import roxanne
import numpy as np

def plotLimitSurface(fileName):
    import os
    
    fileDirectory = os.path.split(fileName)[0]
    plotFileName = os.path.join(fileDirectory, 'limitSurfaceTest.pdf')
    
    fileIn = open(fileName,'r')
    columnDict = roxanne.readDataFileArray(fileIn)
    
    shearForce = columnDict['forceMaxShear']
    normalForce = columnDict['forceMaxAdhesion']
    shearForce = np.array(shearForce)
    normalForce = np.array(normalForce)
    
#     import matplotlib
#     params = {'font.family': 'serif',
#               'font.serif' : 'Computer Modern Roman',
#               'text.usetex': True}
#     matplotlib.rcParams.update(params)
    
    import matplotlib.pyplot
    import matplotlib.axis
    
    
    matplotlib.pyplot.plot(shearForce,normalForce,
                                           linestyle = 'None',
                                           marker = 'o',
                           markerfacecolor = 'w',
                           markeredgecolor = 'g')
    matplotlib.pyplot.xlabel('Shear Force (microNewtons)')
    matplotlib.pyplot.ylabel('Adhesion Force (microNewtons)')
    matplotlib.pyplot.title('Limit Surface')
    matplotlib.pyplot.grid(True)
#    matplotlib.pyplot.axis([0, 5, -3, 3])
    matplotlib.pyplot.savefig(plotFileName,transparent=True)
#    matplotlib.pyplot.show()

    import os
    os.system('open '+plotFileName)

class fileDialog(HasTraits):


    fileName = File
    open = Button('Open')
    view = View(Item('open'),Item('fileName',style='readonly'),width=0.25)
    
    def _open_changed(self):
        fileName = open_file()
        if fileName != '':
            self.fileName = fileName
            plotLimitSurface(self.fileName)
# TODO : format plot with fonts and size

if __name__ == '__main__':
    fileDialog = fileDialog()
    fileDialog.configure_traits()



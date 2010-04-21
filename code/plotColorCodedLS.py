#!/usr/bin/env python

# plotting script that expects a header line with labels for
# each column of data
# these columns of data will be assigned to a dictionary
# returned values are all strings

from enthought.traits.api import HasTraits, Instance, Array, Range, Button, File
from enthought.traits.ui.api import View, Item, Handler
from enthought.traits.ui.menu import OKButton
from enthought.traits.ui.file_dialog import open_file

import roxanne as rx
import numpy as np

class fileDialog(HasTraits):
    fileName = File
    open = Button('Open')
    view = View(Item('open'),Item('fileName',style='readonly'),width=0.25)

    def _open_changed(self):
        fileName = open_file()
        if fileName != '':
            self.fileName = fileName
            plotLimitSurface(self.fileName)

def plotLimitSurface(fileName):
    fileIn = open(fileName,'r')
    columnDict = rx.readDataFileArray(fileIn)
    shearForce = map(float,columnDict['forceMaxShear'])
    normalForce = map(float,columnDict['forceMaxAdhesion'])
    preload = map(float,columnDict['forcePreload'])
    pulloffAngle = map(float,columnDict['pulloffAngle'])

    shearForce = np.array(shearForce)
    normalForce = np.array(normalForce)
    factor = 10
    preload = np.array(preload) * factor
    pulloffAngle = np.array(pulloffAngle)

    import matplotlib.pyplot as plt

    plt.scatter(shearForce,
                normalForce,
                marker = 'o',
                c=pulloffAngle,
                s=preload,
                alpha=0.5)
    plt.xlabel('Shear Force (microNewtons)')
    plt.ylabel('Adhesion Force (microNewtons)')
    plt.title('SPS 06 Limit Surface')
    plt.grid(True)
    colorbar = plt.colorbar()
    colorbar.set_label('angle of pulloff (90 is vertical)')
    plt.savefig('coloredLimitSurface.pdf',transparent=True)


if __name__ == '__main__':
    fileDialog = fileDialog()
    fileDialog.configure_traits()



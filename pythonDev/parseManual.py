#!/usr/bin/env python
# parseManual.py
# python implementation of parse script to find points 

# load in headers using roxanne
# load in data using roxanne

# perform max/min analysis to find points
# store point in Array

import matplotlib.pyplot as mpl
import numpy      as np
import sys
sys.path.append("../roxanne")
import roxanne    as rx

fileName = 'sws10-ls-155936.data'
fileIn = open(fileName,'r')
# header dictionary
hD = rx.readDataFileHeader(fileIn)
# data dictionary
dD = rx.readDataFileArray(fileIn)

voltageLateral        =  map(float,dD['voltageForceLateral'])
voltageNormal         =  map(float,dD['voltageForceNormal'])
positionNormalMicron  =  map(float,dD['voltagePositionX']) * 10
positionLateralMicron =  map(float,dD['voltagePositionY']) * 10

voltageLateral        = -np.array(voltageLateral)
voltageNormal         =  np.array(voltageNormal)
positionNormalMicron  =  np.array(positionNormalMicron) * 10
positionLateralMicron =  np.array(positionLateralMicron) * 10

# cantilever dictionary
cD = rx.getCantileverData(hD['cantilever'])
 
normalStiffness      = cD['normalStiffness']
lateralStiffness     = cD['lateralStiffness']
normalDisplacement   = cD['normalDisplacement']
lateralDisplacement  = cD['lateralDisplacement']
lateralAmplification = float(hD['latAmp'])
normalAmplification  = float(hD['norAmp'])
rollAngle            = float(hD['rollAngle'])
pitchAngle           = float(hD['pitchAngle'])
#anglePulloff         = float(hD['anglePulloff'])
# how do i get parameters from filename

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

# filter spikes



normalForceZip = zip(normalForceMuN,
                     np.arange(len(normalForceMuN)))
indexMaxAdhesion = min(normalForceZip)[1]

normalForceZip = zip(normalForceMuN[0:indexMaxAdhesion],
                     np.arange(indexMaxAdhesion))
indexMaxPreload = max(normalForceZip)[1]

normalForceZip = zip(normalForceMuN[0:indexMaxPreload],
                     np.arange(indexMaxPreload))
indexContact = min(normalForceZip)[1]



mpl.plot(lateralForceMuN,'g')
mpl.plot(normalForceMuN,'b')

mpl.plot([indexMaxPreload],  [normalForceMuN[indexMaxPreload]],'ro')
mpl.plot([indexContact],     [normalForceMuN[indexContact]],'bd')
mpl.plot([indexMaxAdhesion], [normalForceMuN[indexMaxAdhesion]],'gd')

mpl.show()

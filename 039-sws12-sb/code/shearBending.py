import sys
sys.path.append('/Users/dsoto/current/swDataFlat/code')
import roxanne as rx

dataFile = open('../data/separated/039-converted.data','r')
rx.getHeader(dataFile)
data = rx.readDataFileArray(dataFile)

position = data['positionLateralMicron']
force = data['forceLateralMicroNewton']

position = map(float,position)
force = map(float,force)

import matplotlib.pyplot as plt

plt.plot(position,force)

plt.title('039 - SWS 12 Shear Bending')
plt.xlabel('Position (microns)')
plt.ylabel('Force (microNewtons)')
plt.grid()
plt.show()

plt.savefig('039-shearBending.pdf')

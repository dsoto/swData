import sys
sys.path.append('/Users/dsoto/current/swDataFlat/code')
import roxanne as rx

dataFile = open('038-v20-converted.data','r')
rx.getHeader(dataFile)
data = rx.readDataFileArray(dataFile)

position = data['positionLateralMicron']
force = data['forceLateralMicroNewton']

position = map(float,position)
force = map(float,force)

import matplotlib.pyplot as plt

plt.plot(position,force)

plt.title('SPS06 Shear Bending')
plt.xlabel('Position (microns)')
plt.ylabel('Force (microNewtons)')
plt.show()

plt.savefig('test.pdf')

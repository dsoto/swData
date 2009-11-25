'''
this script will plot the timestamps to be sure that the 
roxanne system was able to output at the desire frequency
'''
import matplotlib.pyplot as plt

def plotTime(fileIn):
    rx.readDataFileHeader(fileIn)
    data = rx.readDataFileArray(fileIn)
    
    timeStrings = data['time']
    
    timeSeconds = [float(ts[0:2])*3600+float(ts[3:5])*60+float(ts[6:]) for ts in timeStrings]
    
    import numpy as np
    timeSeconds = np.array(timeSeconds)
    timeSeconds = timeSeconds - timeSeconds[0]
    
    #print timeSeconds
    
    plt.plot(timeSeconds,'o')

import glob
fileNameList = glob.glob('*.data')
for fileName in fileNameList:
    fileIn = open(fileName)
    plotTime(fileIn)

import numpy as np
x = np.array(range(6000))
y = x * 0.010
y1 = x * 0.005
y2 = x * 0.002
y3 = x * 0.001

plt.plot(x,y)
plt.plot(x,y1)
plt.plot(x,y2)
plt.plot(x,y3)

plt.show()
    
'''
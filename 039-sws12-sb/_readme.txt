this directory contains the data for the measurement of the
lateral compliance of the sws12 pdms wedge.

sws12 is a wedge structure



#analysis from ipython
import roxanne as rx
raw = open('039.data','r')
out = open('039-converted.data','w')
rx.convertDataFile(raw,out)
run shearBending.py

#!/usr/bin/env python
from __future__ import print_function
import numpy as np

indices = np.linspace(10859,16558,12)
indices = np.hstack((indices[:-1],np.linspace(16558,22400,12)))
indices = np.hstack((indices[:-1],np.linspace(22400,28474,12)))
indices = np.hstack((indices[:-1],np.linspace(28474,34663,12)))

indices = [10873,11308,11722,12179,12636,13137,13660,14204,14770,15336,15924,16534,16969,17426,17905,18406,18907,19451,19995,20583,21171,21718,22412,22869,23348,23827,24350,24872,25417,26026,26592,27180,27833,28465,28944,29401,29945,30468,30990,31556,32144,32754,33364,34017,34713]


#indices = indices.round(0)
indices = [int(i) for i in indices]

for i in range(len(indices)-1):
    drag = i % 11 * 4
    preload = np.floor(i / 11) * 2 + 29
    print (indices[i],'\t',indices[i+1],'\t', drag,'\t', int(preload))


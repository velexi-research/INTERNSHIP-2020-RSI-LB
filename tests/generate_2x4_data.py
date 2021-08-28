import numpy as np
import random
import os



v1=[1,1,0,0]
v2=[0,0,1,1]
v3=[0,0,0,0]
from random import random

numsamples = 100000

output = np.zeros((numsamples,2*2))
outkeys = np.zeros((numsamples, 2+2))
for i in range(numsamples):
    sample = np.zeros((4))
    key = np.zeros((2+2,))
    r1 = random()
    r2 = random()
    r3 = random()
    maxval = 1
    for j in range(4):
        jsum = v1[j]*r1 + v2[j]*r2 + v3[j]*r3
        output[i,j] = jsum
        if (jsum>maxval):
            maxval = jsum
    if (maxval > 1):
        output[i,:] = output[i,:] / maxval

np.savetxt("../data/data_bin_4.csv", output)

v1=[1,0,0,0]
v2=[0,1,1,1]
v3=[0,0,0,0]

numsamples = 100000

output = np.zeros((numsamples,2*2))
outkeys = np.zeros((numsamples, 2+2))
for i in range(numsamples):
    sample = np.zeros((4))
    key = np.zeros((2+2,))
    r1 = random()
    r2 = random()
    r3 = random()
    maxval = 1
    for j in range(4):
        jsum = v1[j]*r1 + v2[j]*r2 + v3[j]*r3
        output[i,j] = jsum
        if (jsum>maxval):
            maxval = jsum
    if (maxval > 1):
        output[i,:] = output[i,:] / maxval

np.savetxt("../data/data_bin_alt.csv", output)

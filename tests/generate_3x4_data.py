import numpy as np
import random
import os



v1=[0.03656609958318144, 0.7030563533357959, 0.10168774096983756, 0.1586898061111852]
v2=[0.32870294108689874, 0.27198907785827836, 0.3911442937275321, 0.008163687327290801]
v3=[0.3225772487542402, 0.2999037945641546, 0.19936611151524297, 0.17815284516636232]
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
    output[i,:] = output[i,:] / maxval

np.savetxt("../data/data_4.csv", output)

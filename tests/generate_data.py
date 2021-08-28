import numpy as np
import random
import os

numsamples = 100000

output = np.zeros((numsamples,8*8))
outkeys = np.zeros((numsamples, 8+8))
for i in range(numsamples):
    sample = np.zeros((8,8))
    key = np.zeros((16,))
    for j in range(8):
        if (random.random() <= 0.125):
            sample[j,:] = 1
            key[j] = 1
    for j in range(8):
        if (random.random() <= 0.125):
            sample[:,j] = 1
            key[j+8] = 1
    if (random.random() <= 0.5):
        sample[7,:] = 1
        key[7] = 1
    outkeys[i,:] = key
    output[i,:] = sample.reshape((-1))

if not os.path.exists("../data/"):
    os.makedirs("../data/")

np.savetxt("../data/lines_unbalanced.csv", output)
np.savetxt("../data/keys_unbalanced.csv", outkeys)

numsamples = 100000

output = np.zeros((numsamples,8*8))
outkeys = np.zeros((numsamples, 8+8))
for i in range(numsamples):
    sample = np.zeros((8,8))
    key = np.zeros((16,))
    for j in range(8):
        if (random.random() <= 0.125):
            sample[j,:] = 1
            key[j] = 1
    for j in range(8):
        if (random.random() <= 0.125):
            sample[:,j] = 1
            key[j+8] = 1
    outkeys[i,:] = key
    output[i,:] = sample.reshape((-1))

np.savetxt("../data/lines_balanced.csv", output)
np.savetxt("../data/keys_balanced.csv", outkeys)

numsamples = 100000

output = np.zeros((numsamples,2*2))
outkeys = np.zeros((numsamples, 2+2))
for i in range(numsamples):
    sample = np.zeros((2,2))
    key = np.zeros((2+2,))
    for j in range(2):
        if (random.random() <= 0.25):
            sample[j,:] = 1
            key[j] = 1
    for j in range(2):
        if (random.random() <= 0.25):
            sample[:,j] = 1
            key[j+2] = 1
    outkeys[i,:] = key
    output[i,:] = sample.reshape((-1))

np.savetxt("../data/lines_trivial.csv", output)
np.savetxt("../data/keys_trivial.csv", outkeys)

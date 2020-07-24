import numpy as np
from nodes.nodes import FoldiakNode, InputNode
from nodes.net import FoldiakShapedNet
from nodes.layer import ShapedLayer

import random
random.seed(7)

#Builds layers and assembles into a network

inputlayer = ShapedLayer((8,8))
foldiaklayer = ShapedLayer(16)

foldiaklayer.fillnodes(FoldiakNode)
inputlayer.fillnodes(InputNode)

network = FoldiakShapedNet()
network.append(inputlayer)
network.append(foldiaklayer)
network.connect_foldiak(inputlayer, foldiaklayer)

#Integration parameters

network.setparam("intmethod","LSODA")
network.setparam("l",10)
network.setparam("tmax",100)

#Setup network

network.setup()

#Load and shuffle data
samples = np.loadtxt("../data/lines_unbalanced.csv")
keys = np.loadtxt("../data/keys_unbalanced.csv")

perm = np.random.permutation(len(keys))

samples = samples[perm]
keys = keys[perm]

#Train threshold to steady state

network.setparam("a",0.0)
network.setparam("b",0.0)
network.setparam("y",0.5)
network.setparam("d",0.0)

for i in range(200):
    for i in inputlayer.nodes:
        i.setvalstored(random.uniform(0,1))
    network.update()

#Set network parameters

network.setparam("a",0.1)
network.setparam("b",0.02)
network.setparam("y",0.02)
network.setparam("d",0.02)

#Create vectors for use in assigning each output to a line; needed to measure error.

possibletypes = []
for i in range(8):
    sample = np.zeros((8,8))
    sample[i,:] = 1
    possibletypes.append(sample)
for i in range(8):
    sample = np.zeros((8,8))
    sample[:,i] = 1
    possibletypes.append(sample)
    
errors = []

startnum = 0

samples_per_bin = 1000
number_of_bins = 20

for startnum in range(number_of_bins):

    #Assign each memory to a vector; this is needed for measuring error.
    permutation = [0,0,0,0,0,0,0,0,
                   0,0,0,0,0,0,0,0]
    for j in range(16):
        lowestmin = 10000
        goestonum = 0
        tnum = 0
        for i in possibletypes:
            mem = np.reshape(network.cgroups[0].getbiases()[:,j],(8,8))
            mem = mem/mem.max()
            er = np.sum(np.abs(mem - i))
            #print(er)
            if (er < lowestmin):
                lowestmin = er
                goestonum = tnum
            tnum += 1
        permutation[goestonum] = j


    output_keys = np.zeros((samples_per_bin,16))

    idx = np.zeros_like(permutation)
    idx[permutation] = np.arange(len(permutation))

    test_keys_this = keys[startnum*samples_per_bin:startnum*samples_per_bin+samples_per_bin, idx]
    test_samples_this = samples[startnum*samples_per_bin:startnum*samples_per_bin+samples_per_bin]
    
    #Train for samples_per_bin samples
    for i in range(samples_per_bin):
        inputlayer.setvals(test_samples_this[i,:])
        network.update()
        output_keys[i,:] = foldiaklayer.returnvals()

    #Calculate error
    errors.append(np.sum(np.abs(test_keys_this-output_keys))/np.sum(test_keys_this))

    if ((startnum+1)%5)==0:
        print("Finished: " + str((startnum+1)*samples_per_bin))


#Write errors to output.
np.savetxt("../data/errors.csv",np.array(errors))
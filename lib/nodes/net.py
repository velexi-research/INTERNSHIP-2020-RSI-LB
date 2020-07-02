from nodes.core import *
from nodes.connect import *
from nodes.util import *


import numpy as np
import math

class FoldiakNet(net):
    def connect_layer_hebbian(self, layerin, layerout):
        for j in layerout.nodes:
            norm_square_sum = 0
            c_s = []
            for i in layerin.nodes:
                c_to_add = HebbianConnect(i,j)
                self.append_connect(c_to_add)
                
                #Normalize lengths to 1
                c_s.append(c_to_add)
                norm_square_sum += (c_to_add.bias * c_to_add.bias)
            for c in c_s:
                c.bias /= norm_square_sum
    def connect_self_antihebbian(self, layerout):
        for i in layerout.nodes:
            for j in layerout.nodes:
                if (i is not j):
                    self.append_connect(AntiHebbianConnect(i,j))
        self.inihblayers.append(layerout)
    def getimage(self):
        maxpixels = 1
        image = []
        for i in self.layers:
            islayer = False
            try:
                i.val - 1
            except:
                islayer = True
            if islayer:
                if np.lcm(len(i.val), maxpixels) > maxpixels:
                    maxpixels = np.lcm(len(i.val), maxpixels)
        for i in self.layers:
            islayer = False
            try:
                i.val - 1
            except:
                islayer = True
            if islayer:
                thisrow = []
                for j in i.val:
                    for n in range(math.floor(maxpixels/len(i.val))):
                        thisrow.append(j)
                image.append(thisrow)
            else:
                thisrow = []
                for i in range(maxpixels):
                    thisrow.append(i.val)
                image.append(thisrow)
        return(np.uint8(np.array(image)*255))
    def __init__(self):
        self.layers = []
        self.connects = []
        self.valdict = dict()
        self.diffeqs = []
        self.inihblayers = []
    def foldiaksetup(self):
        self.diffeqs = []
        for i in self.layers:
            if i in self.inihblayers:
                self.diffeqs = []
                for node in i.nodes:
                    node.val = 0
                    dq = FoldiakDiffEq(node)
                    self.diffeqs.append(dq)
    def update(self):
        #solve diff eq
        self.foldiaksetup()
        for i in range(self.getdict().get("tnum",100)):
            self.foldiakupdate()
        #update connections, nodes(rounding on nodes)
        for i in self.layers:
            i.update(self.connects)
        for i in self.connects:
            i.update()
    def foldiakupdate(self):
        for i in self.diffeqs:
            i.prop()
        for i in self.diffeqs:
            i.pushval()
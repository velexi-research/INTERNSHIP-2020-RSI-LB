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
                self.pushconnects.append(c_to_add)
                
                #Normalize lengths to 1
                c_s.append(c_to_add)
                norm_square_sum += (c_to_add.bias * c_to_add.bias)
            for c in c_s:
                c.bias /= norm_square_sum
    def connect_self_antihebbian(self, layerout):
        for i in layerout.nodes:
            for j in layerout.nodes:
                if (i is not j):
                    c_to_add = AntiHebbianConnect(i,j)
                    self.append_connect(c_to_add)
                    self.pushconnects.append(c_to_add)
        self.inihblayers.append(layerout)
    def __init__(self):
        self.layers = []
        self.connects = []
        self.valdict = dict()
        self.diffeqs = []
        self.inihblayers = []
        self.pushconnects = []
        self.isinit = False
    def foldiaksetup(self):
        for i in self.diffeqs:
            i.reset()
    def setup(self):
        for i in self.layers:
            i.setup()
        self.diffeqs = []
        for i in self.inihblayers:
            for node in i.nodes:
                dq = FoldiakDiffEq(node)
                node.setsolver(dq)
                self.diffeqs.append(dq)
        for i in self.pushconnects:
            i.pushval()
        self.foldiaksetup()
        self.isinit = True
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
            
            
            
            
            
            
class FoldiakShapedNet(net):
    def connect_foldiak(self, layerin, layerout):
        cg1 = ShapedCGroup(layerin, layerout)
        cg1.mkconnects(HebbianConnect)
        
        cg1.normbiases()
        
        self.cgroups.append(cg1)
        
        
        cg2 = ShapedCGroup(layerout, layerout)
        cg2.mkconnects(AntiHebbianConnect)
        self.cgroups.append(cg2)
        self.inihblayers.append([layerout,cg1,cg2])
    def __init__(self):
        self.layers = []
        self.cgroups = []
        self.connects = []
        self.meta_timing = []
        self.valdict = dict()
        self.inihblayers = []
        self.diffeqs = []
        self.isinit = False
    def setup(self):
        for i in self.layers:
            i.setup()
        self.meta_timing = []
        self.diffeqs = []
        for i in self.inihblayers:
            odesolver = FoldiakShapedDiffEq(i[0], i[1], i[2])
            self.diffeqs.append(odesolver)
        self.isinit = True
    def update(self):
        for i in self.diffeqs:
            i.update()
        for i in self.cgroups:
            i.update()
        for i in self.connects:
            i.update()
        for i in self.layers:
            i.update(self.connects)
    def updatethresonly(self):
        for i in self.diffeqs:
            i.update()
        for i in self.layers:
            i.update(self.connects)
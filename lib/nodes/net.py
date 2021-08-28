from nodes.core import *
from nodes.connect import *
from nodes.util import *


import numpy as np
import math
    
class FoldiakShapedNet(net):
    def connect_foldiak(self, layerin, layerout):
        cg1 = ShapedCGroup(layerin, layerout)
        cg1.mkconnects(HebbianConnect)
        
        cg1.normbiases()
        
        self.cgroups.append(cg1)
        self.inihblayers.append([layerout,cg1])
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
            odesolver = FoldiakShapedDiffEq(i[0], i[1])
            self.diffeqs.append(odesolver)
        self.isinit = True
    def update(self):
        for i in self.diffeqs:
            i.update()
        for i in self.cgroups:
            i.update()
        for i in self.connects:
            i.update()
        for i in self.cgroups:
            i.normbiases()
        for i in self.layers:
            i.update(self.connects)
    def updatethresonly(self):
        for i in self.diffeqs:
            i.update()
        for i in self.layers:
            i.update(self.connects)
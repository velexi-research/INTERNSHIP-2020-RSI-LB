from nodes.core import connect, cgroup
from nodes.layer import ShapedLayer

from random import uniform

import numpy as np

class HebbianConnect(connect):
    def __init__(self, nodein, nodeout):
        self.input = nodein
        self.output = nodeout
        self.bias = uniform(0,1)
    def update(self):
        #hebbian rule
        b = self.getdict().get("b", 0.02)
        dq = b * self.output.val * (self.input.val - self.bias)
        self.bias += dq
    def pushval(self):
        self.output.solver.last_cs.append(self)
    
class AntiHebbianConnect(connect):
    def __init__(self, nodein, nodeout):
        self.input = nodein
        self.output = nodeout
        self.bias = 0.0
    def update(self):
        #anti-hebbian rule
        a = self.getdict().get("a", 0.1)
        p = self.getdict().get("p", 0.1)
        dw = (0-a) * ((self.input.val * self.output.val) - (p*p))
        self.bias += dw
        if (self.bias > 0):
            self.bias = 0
        elif (self.input is self.output):
            self.bias = 0
    def pushval(self):
        self.output.solver.connects.append(self)
        

class ShapedCGroup(cgroup):
    vbias = np.vectorize(lambda i: i.bias)
    vupdate = np.vectorize(lambda i: i.update())
    def __init__(self, layerin, layerout):
        if (not isinstance(layerin, ShapedLayer)) or (not isinstance(layerout, ShapedLayer)):
            raise Exception("Either input or output is the wrong layer type; ShapedLayer needed for ShapedConnectGroup")
        self.connects = []
        self.inshape = layerin.shape
        self.outshape = layerout.shape
        self.shape = (self.inshape+self.outshape)
        self.input = layerin
        self.output = layerout
    def mkconnects(self, initer):
        vinit1 = np.vectorize(initer, excluded = {0})
        vinit = np.vectorize(vinit1, excluded = {1})
        vlist = np.vectorize(lambda i: i.tolist())
        self.npconnects = np.array(vlist(vinit(self.input.npnodes, self.output.npnodes)).tolist())
    def getbiases(self):
        return ShapedCGroup.vbias(self.npconnects)
    def update(self):
        ShapedCGroup.vupdate(self.npconnects)
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
        dw = (0.0-a) * ((self.input.val * self.output.val) - (p*p))
        self.bias += dw
        if (self.bias > 0):
            self.bias = 0.0
        elif (self.input is self.output):
            self.bias = 0.0
    def pushval(self):
        self.output.solver.connects.append(self)
        

class ShapedCGroup(cgroup):
    vbias = np.vectorize(lambda i: i.getbias())
    vupdate = np.vectorize(lambda i: i.update())
    def setnet(i,net):
        i.net = net
    def setbias(i,bias):
        i.bias = bias
    vsetbias = np.vectorize(lambda i,bias: ShapedCGroup.setbias(i,bias))
    vsetnet = np.vectorize((lambda i,net: ShapedCGroup.setnet(i,net)), excluded = {1})
    
    
    
    def __init__(self, layerin, layerout):
        if (not isinstance(layerin, ShapedLayer)) or (not isinstance(layerout, ShapedLayer)):
            raise Exception("Either input or output is the wrong layer type; ShapedLayer needed for ShapedConnectGroup")
        self.connects = []
        self.inshape = layerin.nodes.shape
        self.outshape = layerout.nodes.shape
        self.shape = (self.inshape[0], self.outshape[0])
        self.input = layerin
        self.output = layerout
        self.net = self.input.net
    def mkconnects(self, initer):
        vinit1 = np.vectorize(initer, excluded = {0})
        vinit = np.vectorize(vinit1, excluded = {1})
        vlist = np.vectorize(lambda i: i.tolist())
        self.npconnects = np.array(vlist(vinit(self.input.nodes, self.output.nodes)).tolist())
        ShapedCGroup.vsetnet(self.npconnects, self.input.net)
    def getbiases(self):
        return ShapedCGroup.vbias(self.npconnects)
    def setbiases(self, biases):
        ShapedCGroup.vsetbias(self.npconnects, biases)
    def update(self):
        ShapedCGroup.vupdate(self.npconnects)
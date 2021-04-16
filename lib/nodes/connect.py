from nodes.core import connect, cgroup
from nodes.layer import ShapedLayer

from random import uniform

import numpy as np
import math

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
        p_1 = self.input.p
        p_2 = self.output.p
        dw = (0.0-a) * ((self.input.val * self.output.val) - (p_1*p_2))
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
    def setthres(i, thres):
        i.thres = thres
    vsetbias = np.vectorize(lambda i,bias: ShapedCGroup.setbias(i,bias))
    vsetnet = np.vectorize((lambda i,net: ShapedCGroup.setnet(i,net)), excluded = {1})
    vsetallthres = np.vectorize(lambda i, thres: ShapedCGroup.setthres(i,thres), excluded = {1})
    vsetthres = np.vectorize(lambda i, thres: ShapedCGroup.setthres(i,thres))
    
    
    
    def __init__(self, layerin, layerout):
        if (not isinstance(layerout, ShapedLayer)):
            raise Exception("Output is the wrong layer type; ShapedLayer needed for ShapedConnectGroup")
        if (not isinstance(layerin, ShapedLayer)):
            raise Exception("Input is the wrong layer type; ShapedLayer needed for ShapedConnectGroup")
        self.connects = []
        self.inshape = layerin.nodes.shape
        self.outshape = layerout.nodes.shape
        self.shape = self.inshape + self.outshape
        self.input = layerin
        self.output = layerout
        self.net = self.input.net
        self.insize = 1
        self.outsize = 1
        for i in self.inshape:
            self.insize *= i
        for i in self.outshape:
            self.outsize *= i
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
    def normbiases(self):
        sum_of_rows = np.sqrt(np.square(self.getbiases()).sum(axis=1))
        self.setbiases(self.getbiases() / sum_of_rows[:, np.newaxis])
        


class ShapedFeedingCGroup(ShapedCGroup):
    def update_thres_connect(c, y):
        dt = y * (c.bias)
        c.output.thres += dt
    def zero_thres_node(c):
        c.thres = 0
    vupdatethres = np.vectorize(lambda c, y: ShapedFeedingCGroup.update_thres_connect(c,y), excluded = {1})
    vzerothres = np.vectorize(lambda c: ShapedFeedingCGroup.zero_thres_node(c))
    
    def __init__(self, layerin, layerout):
        super().__init__(layerin, layerout)
    def update(self):
        super().update()
        #y = self.getdict().get("y", 0.02) / self.insize
        y = 0.5 / self.insize
        ShapedFeedingCGroup.vzerothres(self.output.nodes)
        ShapedFeedingCGroup.vupdatethres(self.npconnects,y)
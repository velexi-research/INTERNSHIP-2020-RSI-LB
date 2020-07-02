from math import exp
from numba import jit

#import time

class FoldiakDiffEq:
    def __init__(self,node):
        self.dt = node.getdict().get("dt", 0.1)
        self.t = 0
        self.yi = node.getdict().get("starty", 0.0)
        self.l = node.getdict().get("l", 10)
        self.node = node
        self.connects = []
        self.last_cs = []
        self.net = node.layer.net
        self.pushval()
    def pushval(self):
        self.node.setval(self.yi)
    def prop(self):
        psum = 0
        for i in self.connects:
            psum += i.input.returnval() * i.bias
        inside = psum+self.inside_c
        f = foldiak_func(self.l,inside)
        dy = (f - self.yi)*self.dt
        self.yi += dy
    def reset(self):
        self.yi = node.getdict().get("starty", 0.0)
        self.pushval()
        xqs = 0
        for i in self.last_cs:
            xqs += i.input.returnval() * i.bias
        self.inside_c = xqs - self.node.thres

@jit
def foldiak_func(l, inside):
    return 1.0/(1.0+exp(-1 * l * inside))
from math import exp
from numba import jit
import numpy as np

from scipy.integrate import odeint

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
        self.yi = self.node.getdict().get("starty", 0.0)
        self.pushval()
        xqs = 0
        for i in self.last_cs:
            xqs += i.input.returnval() * i.bias
        self.inside_c = xqs - self.node.thres

@jit(nopython=True, parallel=True)
def foldiak_func(l, inside):
    return 1.0/(1.0+np.exp(-1 * l * inside))


def weightsum(axin, qarr, xarr):
    return np.tensordot(xarr,qarr, axes = axin)
    

    
class FoldiakShapedDiffEq:
    def __init__(self, layer, qgroup, wgroup):
        self.dt = layer.getdict().get("dt", 0.1)
        self.y0 = layer.getdict().get("starty", 0.0)
        self.tnum = layer.getdict().get("tnum",100)
        self.qs = qgroup
        self.ws = wgroup
        self.layer = layer
        self.net = layer.net
        self.l = layer.getdict().get("l", 10)
    def update(self):
        xsum = self.getxsum()
        l = self.l
        yax = len(self.ws.inshape)
        ws = self.ws.getbiases()
        ts = self.layer.returnshapedthres()
        tlin = np.linspace(0,self.dt*self.tnum, num=self.tnum)
        ysum = lambda y: weightsum(yax,
                                   ws, y)
        ode = lambda y,t: foldiak_func(l, xsum - ts + ysum(y)) - y
        #print(ode(np.full(self.layer.shape, self.y0), 0))
        ys = odeint(ode, np.full(self.layer.shape, self.y0), tlin)
        yfinals = np.where(ys > 0.5, 1, 0)
        self.layer.setshapedvals(yfinals)
    def getxsum(self):
        return weightsum(len(self.qs.inshape),
                             self.qs.getbiases(), self.qs.input.returnshapedvals())
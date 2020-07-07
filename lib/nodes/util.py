from math import exp
from numba import jit
import numpy as np

import scipy.integrate

import time

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


def weightsum(xarr, qarr):
    return np.matmul(xarr,qarr)
    

    
class FoldiakShapedDiffEq:
    def __init__(self, layer, qgroup, wgroup):
        self.net = layer.net
        #self.dt = layer.getdict().get("dt", 0.1)
        self.y0 = layer.getdict().get("starty", 0.0)
        #self.tnum = layer.getdict().get("tnum",100)
        self.method = layer.getdict().get("intmethod","LSODA")
        self.qs = qgroup
        self.ws = wgroup
        self.layer = layer
        #self.tlin = np.linspace(0,self.dt*self.tnum, num=self.tnum)
        self.l = layer.getdict().get("l", 10)
        self.trange = (0, layer.getdict().get("tmax", 100))
    def update(self):
        xsum = weightsum(self.qs.input.returnvals(), self.qs.getbiases())
        l = self.l
        yax = len(self.ws.inshape)
        ws = self.ws.getbiases()
        ts = self.layer.returnthres()
        ysum = lambda y: weightsum(y, ws)
        ode = lambda t,y: foldiak_func(l, xsum - ts + ysum(y)) - y
        #print(ode(np.full(self.layer.shape, self.y0), 0))
        #ys = scipy.integrate.odeint(ode, np.full(self.layer.shape, self.y0), self.tlin, tfirst=True)
        #Timing code. comment as needed:
        #t0 = time.clock()
        ys = scipy.integrate.solve_ivp(ode, self.trange, np.full(self.layer.nodes.shape, self.y0), method=self.method).y[:,-1]
        #t1 = time.clock()
        #tdiff = t1-t0
        #self.net.meta_timing.append(tdiff)
        yfinals = np.where(ys > 0.5, 1, 0)
        self.layer.setvals(yfinals)
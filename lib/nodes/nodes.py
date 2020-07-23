from nodes.core import node

import random
import math
import statistics
import numpy as np

class FoldiakNode(node):
    def __init__(self, thres=0.5):
        self.val = 0
        self.thres = thres
        self.layer = None
        self.solver = None
        self.p = self.getdict().get("p", 0.5)
        self.cert = 0
    def setup(self, thres=0.5):
        self.val = 0
        self.thres = thres
        self.p = self.getdict().get("p", 0.5)
        self.cert = 0
    def update(self, connects):
        #round value
        #if self.val > 0.5:
        #    self.val = 1
        #else:
        #    self.val = 0
        #threshold modification
        y = self.getdict().get("y", 0.02)
        dt = y * (self.val - self.p)
        self.thres += dt
        
        d = self.getdict().get("d", 0.02)
        dp = d * (self.val - self.p) * abs(1.0 - self.cert)
        self.p += dp
        
        
        #certainty
        #ideas:
        #if y = 1, c = p
        #if y = 0, c = 1-p
        #cnew = |1-y-p|
        #however, this averages to c = 0.5. I want something that will approach c=1 over time as E(y_i) aproaches p.
        #y-p -> 0, so (1-y+p) -> 1
        #what if c -> 1, with c_new = (cr * (1-y+p)) + ((1-cr) * c_old)
        #and then use |p-c|/p in the p rule.
        cr = self.getdict().get("cr", 0.0)
        self.cert = (cr * (1.0 - self.val + self.p)) + ((1-cr) * self.cert)
        #self.p = self.thres
    def evaluate(self, connects):
        pass
    def setsolver(self, solver):
        self.solver = solver

                
                
                
                
class InputNode(node):
    def __init__(self, value):
        self.val = value
        self.valstored = value
        self.layer = None
    def __init__(self):
        value = 0
        self.val = value
        self.valstored = value
        self.layer = None
    def update(self, connects):
        self.val = self.valstored
    def evaluate(self, connects):
        self.val = self.valstored
    def setvalstored(self, valstored):
        self.valstored = valstored
        self.val = valstored
    def setval(self, valstored):
        self.valstored = valstored
        self.val = valstored


class NullNode(node):
    def __init__(self):
        self.val = 0
        self.layer = None
    def update(self, connects):
        self.val = 0
    def evaluate(self, connects):
        self.val = 0
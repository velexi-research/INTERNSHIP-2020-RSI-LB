from nodes.core import connect

from random import uniform

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
    def pushval(self):
        self.output.solver.connects.append(self)
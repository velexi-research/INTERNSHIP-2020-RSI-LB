from nodes.core import connect

from random import uniform

class HebbianConnect(connect):
    def __init__(self, nodein, nodeout):
        self.input = nodein
        self.output = nodeout
        self.bias = uniform(0,1)
    def update(self):
        #hebbian rule
        b = self.valdict.get("b", default=0.1)
        dq = b * nodeout.val * (nodein.val - self.bias)
        self.bias += dq
    
class AntiHebbianConnect(connect):
    def __init__(self, nodein, nodeout):
        self.input = nodein
        self.output = nodeout
        self.bias = 0.0
    def update(self):
        #anti-hebbian rule
        a = self.valdict.get("a", default=0.1)
        p = self.valdict.get("p", default=0.1)
        dw = (0-a) * ((nodein.val * nodeout.val) - (p*p))
        self.bias += dw
        if (self.bias > 0):
            self.bias = 0
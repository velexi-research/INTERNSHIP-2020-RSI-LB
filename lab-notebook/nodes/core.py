import numbers
from random import choice
import random

class net:
    def __init__(self):
        self.layers = []
        self.connects = []
    def update(self, numiter):
        for i in range(numiter):
            for i in self.nodes[::-1]:
                i.update(self.connects)
    def evaluate(self, numiter):
        for i in range(numiter):
            for i in self.nodes[::-1]:
                i.evaluate(self.connects)
    def append(self, layer):
        self.layers.append(layer)
    def returnvals(self):
        vals = []
        for i in self.layers:
            vals.append(i.val)
        return vals

                
class connect:
    def __init__(self, nodein, nodeout):
        self.input = nodein
        self.output = nodeout
        self.bias = 1.0
    def update(self):
        pass
    def getval(self):
        return input.returnval()*self.bias
    def to(node):
        return (node is self.output)
    def fr(node):
        return (node is self.input)
                
                
                
class node:
    def __init__(self):
        self.val = 0
    def returnval(self):
        return self.val
    def update(self, connects):
        pass
    def setval(self, val):
        self.val = val
    def evaluate(self, connects):
        pass


class layer:
    def __init__(self, nodes):
        self.nodes = nodes
        self.val = self.returnvals()
    def update(self, connects):
        for i in self.nodes:
            i.update(connects)
        self.val = self.returnvals()
    def evaluate(self, connects):
        for i in self.nodes:
            i.evaluate(connects)
        self.val = self.returnvals()
    def append(self, node):
        self.nodes.append(node)
        self.val = self.returnvals()
    def returnvals(self):
        vals = []
        for i in self.nodes:
            vals.append(i.val)
        return vals
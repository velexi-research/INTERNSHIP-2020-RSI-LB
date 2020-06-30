import numbers
from random import choice
import random

nodes_empty_default_dict = dict()

class core:
    def updatedicts(self):
        pass
    def setdict(self, dictin):
        pass

class net(core):
    def __init__(self):
        self.layers = []
        self.connects = []
        self.valdict = dict()
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
        self.updatedicts()
    def append_connect(self, connect):
        self.connects.append(connect)
        self.updatedicts_connect()
    def returnvals(self):
        vals = []
        for i in self.layers:
            vals.append(i.val)
        return vals
    def setdict(self, dictin):
        self.valdict = dictin
    def updatedicts(self):
        for i in self.layers:
            i.setdict(self.valdict)
            i.updatedicts()
    def updatedicts_connect(self):
        for i in self.connects:
            i.setdict(self.valdict)
            i.updatedicts()

                
class connect(core):
    def __init__(self, nodein, nodeout):
        self.input = nodein
        self.output = nodeout
        self.bias = 1.0
        self.valdict = nodes_empty_default_dict
    def update(self):
        pass
    def getval(self):
        return input.returnval()*self.bias
    def to(node):
        return (node is self.output)
    def fr(node):
        return (node is self.input)
    def setdict(self, dictin):
        self.valdict = dictin
                
                
                
class node(core):
    def __init__(self):
        self.val = 0
        self.valdict = nodes_empty_default_dict
    def returnval(self):
        return self.val
    def update(self, connects):
        pass
    def setval(self, val):
        self.val = val
    def evaluate(self, connects):
        pass
    def setdict(self, dictin):
        self.valdict = dictin


class layer(core):
    def __init__(self):
        self.nodes = []
        self.val = self.returnvals()
        self.valdict = nodes_empty_default_dict
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
        self.updatedicts()
    def returnvals(self):
        vals = []
        for i in self.nodes:
            vals.append(i.val)
        return vals
    def updatedicts(self):
        for i in self.nodes:
            i.setdict(self.valdict)
            i.updatedicts()
    def setdict(self, dictin):
        self.valdict = dictin
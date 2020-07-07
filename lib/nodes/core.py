import numbers
from random import choice
import random

nodes_empty_default_dict = dict()

class core:
    def getdict(self):
        return nodes_empty_default_dict

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
        layer.net = self
    def append_connect(self, connect):
        self.connects.append(connect)
        connect.net = self
    def returnvals(self):
        vals = []
        for i in self.layers:
            vals.append(i.val)
        return vals
    def setdict(self, dictin):
        self.valdict = dictin
    def getdict(self):
        return self.valdict
    def setparam(self,key, val):
        self.valdict[key] = val
    def setup(self):
        pass

                
class connect(core):
    def __init__(self, nodein, nodeout):
        self.input = nodein
        self.output = nodeout
        self.bias = 1.0
        self.net = None
    def update(self):
        pass
    def getval(self):
        return input.returnval()*self.bias
    def to(self, node):
        return (node is self.output)
    def fr(self, node):
        return (node is self.input)
    def getdict(self):
        try:
            return self.net.getdict()
        except Exception:
            return nodes_empty_default_dict
    def getbias(self):
        return self.bias
                
                
                
class node(core):
    def __init__(self):
        self.val = 0
        self.layer = None
        self.thres = 0
    def returnval(self):
        return self.val
    def update(self, connects):
        pass
    def setval(self, val):
        self.val = val
    def evaluate(self, connects):
        pass
    def getdict(self):
        try:
            return self.layer.net.getdict()
        except Exception:
            return nodes_empty_default_dict


class layer(core):
    def __init__(self):
        self.nodes = []
        self.val = self.returnvals()
        self.valdict = nodes_empty_default_dict
        self.net = None
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
        node.layer = self
        self.val = self.returnvals()
    def returnvals(self):
        vals = []
        for i in self.nodes:
            vals.append(i.val)
        return vals
    def getdict(self):
        try:
            return self.net.getdict()
        except Exception:
            return nodes_empty_default_dict

class cgroup(core):
    def __init__(self):
        self.connects = []
        self.valdict = nodes_empty_default_dict
        self.net = None
    def update(self):
        for i in self.connects:
            i.update()
    def getdict(self):
        try:
            return self.net.getdict()
        except Exception:
            return nodes_empty_default_dict
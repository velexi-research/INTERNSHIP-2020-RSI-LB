from nodes.core import node

import random
import math
import statistics
import numpy as np

class FoldiakNode(node):
    def __init__(self):
        self.val = 0
        #self.thres = self.getdict().get("p", 0.5)
        self.thres = 0.0
        self.layer = None
        self.solver = None
        #self.p = self.getdict().get("p", 0.5)
    def setup(self):
        self.val = 0
        #self.thres = self.getdict().get("p", 0.5)
        self.thres = 0.0
        #self.p = self.getdict().get("p", 0.5)
    def update(self, connects):
        #round value
        #if self.val > 0.5:
        #    self.val = 1
        #else:
        #    self.val = 0
        #threshold modification
        #y = self.getdict().get("y", 0.02)
        #dt = y * (self.val-0.125)
        #dt = y * (self.val-self.p)
        #self.thres += dt
        
        #d = self.getdict().get("d", 0.02)
        #dp = d * (self.val-self.p)
        #dp = d * math.sin((self.val - self.p)*math.pi/2.0) / self.thres
        #dp = d * (self.val-0.5) * (self.val-self.p)**2;
        #self.p += dp
        pass
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
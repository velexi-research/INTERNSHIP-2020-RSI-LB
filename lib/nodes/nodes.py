from nodes.core import node

import random
import math
import statistics
import numpy as np

class FoldiakNode(node):
    def __init__(self, thres):
        self.val = 0
        self.thres = thres
        self.layer = None
        self.solver = None
    def update(self, connects):
        #round value
        if self.val > 0.5:
            self.val = 1
        else:
            self.val = 0
        #threshold modification
        y = self.getdict().get("y", 0.02)
        p = self.getdict().get("p", 0.1)
        dt = y * (self.val - p)
        self.thres += dt
    def evaluate(self, connects):
        pass
    def setsolver(self, solver):
        self.solver = solver

                
                
                
                
class InputNode(node):
    def __init__(self, value):
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
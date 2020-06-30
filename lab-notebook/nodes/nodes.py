from nodes.core import node

import random
import math
import statistics
import numpy as np

class FoldiakNode(node):
    def __init__(self, nodesin, thres):
        self.val = 0
        self.connections = nodesin
        self.biases = [1.0] * len(nodesin)
        self.thres = thres
    def update(self, connects):
        pass
    def evaluate(self, connects):
        if len(connects) != 0:
            val = 0
            for j in range(len(connects)):
                i = connects[j]
                if(i.to(self)):
                    val += i.getval()
            if val > thres:
                self.val = 1
            else:
                self.val = 0

                
                
                
                
class InputNode(node):
    def __init__(self, value):
        self.connections = []
        self.biases = []
        self.val = value
    def append(self, node):
        self.connections = []
    def update(self):
        self.val = self.val
    def evaluate(self):
        self.val = self.val
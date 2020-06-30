from nodes.core import connect

class HebbianConnect(connect):
    def __init__(self, nodein, nodeout):
        self.input = nodein
        self.output = nodeout
        self.bias = 1.0
    def update(self):
        pass
    
    
class AntiHebbianConnect(connect):
    def __init__(self, nodein, nodeout):
        self.input = nodein
        self.output = nodeout
        self.bias = 1.0
    def update(self):
        pass
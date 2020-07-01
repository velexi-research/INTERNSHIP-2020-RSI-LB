from math import exp

class FoldiakDiffEq:
    def __init__(self,node):
        self.dt = node.getdict().get("dt", 0.1)
        self.t = 0
        self.yi = node.getdict().get("starty", 0.0)
        self.node = node
        self.connects = []
        self.net = node.layer.net
        xqs = []
        for i in self.net.connects:
            if (i.output is self.node) and (i.input.layer is self.node.layer):
                self.connects.append(i)
            elif (i.output is self.node) and (i.input.layer is not self.node.layer):
                xqs.append(i.input.returnval() * i.bias)
        self.inside_c = sum(xqs) - node.thres
        self.pushval()
    def pushval(self):
        self.node.setval(self.yi)
    def prop(self):
        products = []
        for i in self.connects:
            products.append(i.input.returnval() * i.bias)
        yj = sum(products)
        l = self.net.getdict().get("l", 10)
        inside = yj+self.inside_c
        f = 1.0/(1.0+exp(-1 * l * inside))
        dy = (f - self.yi)*self.dt
        self.yi += dy
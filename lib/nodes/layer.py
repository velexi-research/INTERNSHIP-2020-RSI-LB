import numpy as np
from nodes.core import layer, nodes_empty_default_dict
from nodes.nodes import NullNode

class ShapedLayer(layer):
    vtgetter = np.vectorize(lambda i: i.thres)
    vvalgetter = np.vectorize(lambda i: i.val)
    vvalsetter = np.vectorize(lambda ar, v: ar.setval(v))
    def __init__(self, shape):
        if not isinstance(shape, tuple):
            shape = (shape,)
        self.valdict = nodes_empty_default_dict
        self.net = None
        self.shape = shape
        self.setupnodes()
        self.val = self.returnvals()
    def setupnodes(self):
        self.npnodes = np.empty(self.shape, dtype=object)
        self.npnodes[:] = NullNode()
        self.u_nodelist()
    def fillnodes(self, iner):
        vin = np.vectorize(lambda i: iner())
        self.npnodes = vin(self.npnodes)
        self.u_nodelist()
    def u_nodelist(self):
        self.nodes = np.reshape(self.npnodes,-1)
    def update(self, connects):
        for i in self.nodes:
            i.update(connects)
        self.val = self.returnvals()
    def evaluate(self, connects):
        for i in self.nodes:
            i.evaluate(connects)
        self.val = self.returnvals()
    def append(self, node):
        raise(Exception("Nodes cannot be appended to a ShapedLayer. Try replacing an existing node, and make sure to call u_nodelist() after changing a node."))
    def returnvals(self):
        return (ShapedLayer.vvalgetter(self.nodes))
    def returnshapedvals(self):
        return (ShapedLayer.vvalgetter(self.npnodes))
    def returnshapedthres(self):
        return (ShapedLayer.vtgetter(self.npnodes))
    def returnthres(self):
        return (ShapedLayer.vtgetter(self.nodes))
    def setshapedvals(self, vals):
        ShapedLayer.vvalsetter(self.npnodes, vals)
    def setvals(self, vals):
        ShapedLayer.vvalsetter(self.nodes, vals)
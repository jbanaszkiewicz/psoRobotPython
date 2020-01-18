import numpy as np


def loadGraph(filename):
    nodes = []
    for line in open(filename, 'r'):
        nodes.append(float(line))

    nrNodes = int(nodes.pop(0))

    neighborhood = nodes.pop(0)

    nodes = np.reshape(nodes, newshape=(int(len(nodes)/2), 2))
    return nrNodes, neighborhood, nodes

def generateEdges(nodes, neighborhood):
    edges = np.zeros(shape=(len(nodes),len(nodes)))
    for idxP, p in enumerate(nodes):
        for idxQ, q in enumerate(nodes):
            distance = normSquared(p,q)
            if idxP != idxQ and distance <= neighborhood:
                edges[idxP, idxQ] = distance
            else:
                edges[idxP, idxQ] = -1
    return edges

def normSquared(p, q):

    return np.square((p[0] - q[0])*(p[0] - q[0]) + (p[1] - q[1])*(p[1] - q[1]))

import graph
from copy import deepcopy
import numpy as np


nrParticles = 2
filename = r'./graphs/graph100'
nrNodes, neighborhood, nodes = graph.loadGraph(filename)
edges = graph.generateEdges(nodes, neighborhood)

pso(nodes, edges, nrParticles)

##pso search


import graph
from copy import deepcopy
import numpy as np
import pso


nrParticles = 2
nrIterations = 3
filename = r'./graphs/graph100'
nrNodes, neighborhood, nodes = graph.loadGraph(filename)
edges = graph.generateEdges(nodes, neighborhood)

pso.pso(nodes, edges, nrParticles, nrIterations)

##pso search


import graph
import numpy as cu
import pso
import time

nrParticles = 200
nrIterations = 10
filename = r'./graphs/graph100'
nrNodes, neighborhood, nodes = graph.loadGraph(filename)
edges = graph.generateEdges(nodes, neighborhood)



s = time.time()
pso.pso(nodes, edges, nrParticles, nrIterations)
f = time.time()
print(f-s)



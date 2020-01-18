import graph
import cupy as cu
import pso


nrParticles = 2
nrIterations = 3
filename = r'./graphs/graph100'
nrNodes, neighborhood, nodes = graph.loadGraph(filename)
edges = graph.generateEdges(nodes, neighborhood)

nodes = cu.asarray(nodes)
edges = cu.asarray(edges)

pso.pso(nodes, edges, nrParticles, nrIterations)

##pso search


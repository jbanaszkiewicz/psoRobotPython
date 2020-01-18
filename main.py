import graph
import path
from copy import deepcopy


nrParticles = 2
filename = r'./graphs/graph100'
nrNodes, neighborhood, nodes = graph.loadGraph(filename)
edges = graph.generateEdges(nodes, neighborhood)

randomPaths = path.getRandomPaths(edges, nodes, nrParticles)
bestPaths = deepcopy(randomPaths)
bestPathGlobal = deepcopy(bestPaths[0])


##pso search

